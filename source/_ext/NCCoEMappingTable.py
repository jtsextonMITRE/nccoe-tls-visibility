from __future__ import annotations

import csv
from urllib.request import urlopen
from urllib.error import URLError
import warnings

from docutils import nodes, statemachine
from docutils.io import FileInput, StringInput
from docutils.parsers.rst import Directive, directives
from docutils.parsers.rst.directives import images, tables
from docutils.parsers.rst.directives.misc import adapt_path
from docutils.parsers.rst.directives.tables import align, Table
from docutils.utils import SystemMessagePropagation

from sphinx.application import Sphinx
from sphinx.util.docutils import SphinxDirective, SphinxRole
from sphinx.util.typing import ExtensionMetadata

class NCCoEMappingTable(Table):

    option_spec = {'header-rows': directives.nonnegative_int,
                   'stub-columns': directives.nonnegative_int,
                   'header': directives.unchanged,
                   'width': directives.length_or_percentage_or_unitless,
                   'widths': directives.value_or(('auto', ),
                                                 directives.positive_int_list),
                   'file': directives.path,
                   'url': directives.uri,
                   'encoding': directives.encoding,
                   'class': directives.class_option,
                   'name': directives.unchanged,
                   'align': align,
                   # field delimiter char
                   'delim': directives.single_char_or_whitespace_or_unicode,
                   # treat whitespace after delimiter as significant
                   'keepspace': directives.flag,
                   # text field quote/unquote char:
                   'quote': directives.single_char_or_unicode,
                   # char used to escape delim & quote as-needed:
                   'escape': directives.single_char_or_unicode}

    class DocutilsDialect(csv.Dialect):

        """CSV dialect for `csv_table` directive."""

        delimiter = ','
        quotechar = '"'
        doublequote = True
        skipinitialspace = True
        strict = True
        lineterminator = '\n'
        quoting = csv.QUOTE_MINIMAL

        def __init__(self, options) -> None:
            if 'delim' in options:
                self.delimiter = options['delim']
            if 'keepspace' in options:
                self.skipinitialspace = False
            if 'quote' in options:
                self.quotechar = options['quote']
            if 'escape' in options:
                self.doublequote = False
                self.escapechar = options['escape']
            super().__init__()

    class HeaderDialect(csv.Dialect):
        """
        CSV dialect used for the "header" option data.

        Deprecated. Will be removed in Docutils 0.22.
        """
        # The separate HeaderDialect was introduced in revision 2294
        # (2004-06-17) in the sandbox before the "csv-table" directive moved
        # to the trunk in r2309. Discussion in docutils-devel around this time
        # did not mention a rationale (part of the discussion was in private
        # mail).
        # This is in conflict with the documentation, which always said:
        # "Must use the same CSV format as the main CSV data."
        # and did not change in this aspect.
        #
        # Maybe it was intended to have similar escape rules for rST and CSV,
        # however with the current implementation this means we need
        # `\\` for rST markup and ``\\\\`` for a literal backslash
        # in the "option" header but ``\`` and ``\\`` in the header-lines and
        # table cells of the main CSV data.
        delimiter = ','
        quotechar = '"'
        escapechar = '\\'
        doublequote = False
        skipinitialspace = True
        strict = True
        lineterminator = '\n'
        quoting = csv.QUOTE_MINIMAL

        def __init__(self) -> None:
            warnings.warn('CSVTable.HeaderDialect will be removed '
                          'in Docutils 1.0',
                          DeprecationWarning, stacklevel=2)
            super().__init__()

    @staticmethod
    def check_requirements() -> None:
        warnings.warn('CSVTable.check_requirements()'
                      ' is not required with Python 3'
                      ' and will be removed in Docutils 0.22.',
                      DeprecationWarning, stacklevel=2)

    def process_header_option(self):
        source = self.state_machine.get_source(self.lineno - 1)
        table_head = []
        max_header_cols = 0
        if 'header' in self.options:   # separate table header in option
            rows, max_header_cols = self.parse_csv_data_into_rows(
                                        self.options['header'].split('\n'),
                                        self.DocutilsDialect(self.options),
                                        source)
            table_head.extend(rows)
        return table_head, max_header_cols

    def run(self):
        try:
            if (not self.state.document.settings.file_insertion_enabled
                and ('file' in self.options
                     or 'url' in self.options)):
                warning = self.reporter.warning('File and URL access '
                    'deactivated; ignoring "%s" directive.' % self.name,
                    nodes.literal_block(self.block_text, self.block_text),
                    line=self.lineno)
                return [warning]
            title, messages = self.make_title()
            csv_data, source = self.get_csv_data()
            table_head, max_header_cols = self.process_header_option()
            rows, max_cols = self.parse_csv_data_into_rows(
                csv_data, self.DocutilsDialect(self.options), source)
            max_cols = max(max_cols, max_header_cols)
            header_rows = self.options.get('header-rows', 0)
            stub_columns = self.options.get('stub-columns', 0)
            self.check_table_dimensions(rows, header_rows, stub_columns)
            table_head.extend(rows[:header_rows])
            table_body = rows[header_rows:]
            col_widths = self.get_column_widths(max_cols)
            self.extend_short_rows_with_empty_cells(max_cols,
                                                    (table_head, table_body))
        except SystemMessagePropagation as detail:
            return [detail.args[0]]
        except csv.Error as detail:
            message = str(detail)
            error = self.reporter.error('Error with CSV data'
                ' in "%s" directive:\n%s' % (self.name, message),
                nodes.literal_block(self.block_text, self.block_text),
                line=self.lineno)
            return [error]
        table = (col_widths, table_head, table_body)
        table_node = self.state.build_table(table, self.content_offset,
                                            stub_columns, widths=self.widths)
        table_node['classes'] += self.options.get('class', [])
        if 'align' in self.options:
            table_node['align'] = self.options.get('align')
        self.set_table_width(table_node)
        self.add_name(table_node)
        if title:
            table_node.insert(0, title)
        return [table_node] + messages

    def get_csv_data(self):
        """
        Get CSV data from the directive content, from an external
        file, or from a URL reference.
        """
        settings = self.state.document.settings
        encoding = self.options.get('encoding', settings.input_encoding)
        error_handler = settings.input_encoding_error_handler
        if self.content:
            # CSV data is from directive content.
            if 'file' in self.options or 'url' in self.options:
                error = self.reporter.error('"%s" directive may not both '
                    'specify an external file and have content.' % self.name,
                    nodes.literal_block(self.block_text, self.block_text),
                    line=self.lineno)
                raise SystemMessagePropagation(error)
            source = self.content.source(0)
            csv_data = self.content
        elif 'file' in self.options:
            # CSV data is from an external file.
            if 'url' in self.options:
                error = self.reporter.error('The "file" and "url" options '
                    'may not be simultaneously specified '
                    'for the "%s" directive.' % self.name,
                    nodes.literal_block(self.block_text, self.block_text),
                    line=self.lineno)
                raise SystemMessagePropagation(error)
            source = adapt_path(self.options['file'],
                                self.state.document.current_source,
                                settings.root_prefix)
            try:
                csv_file = FileInput(source_path=source,
                                     encoding=encoding,
                                     error_handler=error_handler)
                csv_data = csv_file.read().splitlines()
            except OSError as error:
                severe = self.reporter.severe(
                    'Problems with "%s" directive path:\n%s.'
                    % (self.name, error),
                    nodes.literal_block(self.block_text, self.block_text),
                    line=self.lineno)
                raise SystemMessagePropagation(severe)
            else:
                settings.record_dependencies.add(source)
        elif 'url' in self.options:
            source = self.options['url']
            try:
                with urlopen(source) as response:
                    csv_text = response.read()
            except (URLError, OSError, ValueError) as error:
                severe = self.reporter.severe(
                      'Problems with "%s" directive URL "%s":\n%s.'
                      % (self.name, self.options['url'], error),
                      nodes.literal_block(self.block_text, self.block_text),
                      line=self.lineno)
                raise SystemMessagePropagation(severe)
            csv_file = StringInput(source=csv_text, source_path=source,
                                   encoding=encoding,
                                   error_handler=error_handler)
            csv_data = csv_file.read().splitlines()
        else:
            error = self.reporter.warning(
                'The "%s" directive requires content; none supplied.'
                % self.name,
                nodes.literal_block(self.block_text, self.block_text),
                line=self.lineno)
            raise SystemMessagePropagation(error)
        return csv_data, source

    def parse_csv_data_into_rows(self, csv_data, dialect, source):
        csv_reader = csv.reader((line + '\n' for line in csv_data),
                                dialect=dialect)
        rows = []
        max_cols = 0
        for row in csv_reader:
            row_data = []
            for cell in row:
                cell_data = (0, 0, 0, statemachine.StringList(
                    cell.splitlines(), source=source))
                row_data.append(cell_data)
            rows.append(row_data)
            max_cols = max(max_cols, len(row))
        return rows, max_cols

def setup(app: Sphinx) -> ExtensionMetadata:
    app.add_directive('nccoe-mapping-table', NCCoEMappingTable)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }