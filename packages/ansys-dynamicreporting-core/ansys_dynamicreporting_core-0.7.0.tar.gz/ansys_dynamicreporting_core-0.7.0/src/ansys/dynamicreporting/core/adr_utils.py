import logging
import sys

# Dictionary to match:
# key: ADR DataItem type
# value: ADR item_* field
dict_items = {
    "animation": "item_animation",
    "file": "item_file",
    "html": "item_text",
    "image": "item_image",
    "string": "item_text",
    "scene": "item_scene",
    "table": "item_table",
    "tree": "item_tree",
}

# Dictionary to match:
# key: ADR item_* field
# value: ADR DataItem type
# (inverse of dict_items
type_maps = {
    "item_text": "text",
    "item_scene": "scene",
    "item_image": "image",
    "item_table": "table",
    "item_animation": "animation",
    "item_file": "file",
    "item_tree": "tree",
}

# Table attributes. To be generated by the read_prop.py file
table_attr = (
    "format",
    "format_column",
    "labels_column",
    "format_row",
    "labels_row",
    "plot",
    "title",
    "line_color",
    "line_marker",
    "line_marker_text",
    "marker_text_rowname",
    "line_marker_size",
    "line_marker_opacity",
    "line_marker_scale",
    "line_error_bars",
    "line_marker_aux0",
    "line_marker_aux1",
    "line_marker_aux2",
    "line_marker_aux3",
    "line_marker_aux4",
    "line_marker_aux5",
    "line_marker_aux6",
    "line_marker_aux7",
    "line_marker_aux8",
    "line_marker_aux9",
    "column_minimum",
    "column_maximum",
    "line_style",
    "line_width",
    "stacked",
    "bar_mode",
    "xaxis",
    "yaxis",
    "palette",
    "palette_position",
    "palette_range",
    "palette_show",
    "palette_title",
    "histogram_threshold",
    "histogram_cumulative",
    "histogram_normalized",
    "histogram_bin_size",
    "bar_gap",
    "width",
    "height",
    "show_legend",
    "legend_position",
    "show_legend_border",
    "show_border",
    "plot_margins",
    "plot_title",
    "plot_xaxis_type",
    "plot_yaxis_type",
    "xrange",
    "yrange",
    "xaxis_format",
    "yaxis_format",
    "xtitle",
    "ytitle",
    "item_justification",
    "nan_display",
    "table_sort",
    "table_title",
    "align_column",
    "table_search",
    "table_page",
    "table_pagemenu",
    "table_scrollx",
    "table_scrolly",
    "table_bordered",
    "table_condensed",
    "table_wrap_content",
    "table_default_col_labels",
    "table_cond_format",
    "row_tags",
    "col_tags"
)


def in_ipynb():
    try:
        ipy_str = str(type(get_ipython()))
        if "zmqshell" in ipy_str:
            return True
        if "terminal" in ipy_str:
            return False
    except Exception:  # todo: please specify the possible exceptions here.
        return False


def get_logger(logfile=None):
    """
    Create a logger for ``pydynamicreporting`` if it does not exist already.

    Parameters
    ----------
        logfile: str
            Name of the file for the log. If none, then use default stream

    Return
    ------
        logger: logging.logger
            The logger object.
    """
    logger = logging.getLogger()
    logger.setLevel(logging.ERROR)
    if logfile is None:
        # Logging for Python APIs should be disabled by default
        ch = logging.NullHandler()
    elif logfile=='stdout':
        ch = logging.StreamHandler(sys.stdout)
    else:
        ch = logging.FileHandler(logfile)
    ch.setLevel(logging.ERROR)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger


def check_filter(filter: str = ""):
    """
    Verify validity of the query string for filtering.

    Parameters
    ----------
    filter : str, optional
        Query string for filtering. The default is ``""``. The syntax corresponds
        to the syntax for Ansys Dynamic Reporting. For more information, see
        _Query Expressions in the documentation for Ansys Dynamic Reporting.

    Returns
    -------
    bool
        ``True`` if the query string is valid, ``False`` otherwise.
    """
    for query_stanza in filter.split(";"):
        if len(query_stanza) > 0:
            if len(query_stanza.split("|")) != 4:
                return False
            if query_stanza.split("|")[0] not in ["A", "O"]:
                return False
            if query_stanza.split("|")[1][0:2] not in ["i_", "s_", "d_", "t_"]:
                return False
    return True


def build_query_url(logger = None, filter: str = "") -> str:
    """
    Build the query section of report url.

    Parameters
    ----------
    logger: logging.logger
        The logger object.

    filter : str, optional
        Query string for filtering. The default is ``""``. The syntax corresponds
        to the syntax for Ansys Dynamic Reporting. For more information, see
        _Query Expressions in the documentation for Ansys Dynamic Reporting.

    Returns
    -------
    str
        query section of the report url corresponding to the query string.
    """
    valid = check_filter(filter)
    if valid is False:
        logger.warning("Warning: filter string is not valid. Will be ignored.")
        return ""
    else:
        query_str = "&query={}".format(filter.replace("|", "%7C").replace(";", "%3B").replace("&", "%2C"))
        return query_str
