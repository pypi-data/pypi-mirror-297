#!/usr/bin/env python
"""

Zotero utils and highlights manager in sioyek PDF reader.

Author: eduardotcampos@usp.br

Based on pyzotero and sqlite3.

=======
CONFIGS
=======

To use this script define the variables in this script or as environment variables:

ZOTERO_LIBRARY_ID: Your personal library ID available in https://www.zotero.org/settings/keys,
in the section Your userID for use in API calls.

ZOTERO_API_KEY: Api key, you can obtain in https://www.zotero.org/settings/keys/new.

ZOTERO_LIBRARY_TYPE: Zotero library type, can be 'user' or 'group'.

SIOYEK_LOCAL_DATABASE_FILE_PATH: Sioyek .db local database file path.

SIOYEK_SHARED_DATABASE_FILE_PATH: Sioyek .db shared database file path.

SIOYEK_PATH: Sioyek program path.

ZOTERO_TO_SIOYEK_COLORS: Sioyek highlight type letter associated to each zotero highlight color.

ZOTERO_LOCAL_DIR: Zotero local PDFs directory like 'home/user/Zotero/storage'

"""

import argparse
import ast
import datetime
import hashlib
import json
import os
import pathlib
import re
import sqlite3
import subprocess
import sys
import textwrap
import uuid
from collections.abc import Sequence
from difflib import SequenceMatcher
from os import path
from typing import NamedTuple, Optional, TypedDict, Union

import fitz
from pyzotero import zotero
from sioyek.sioyek import AbsoluteDocumentPos, Sioyek, clean_path

ZOTERO_LIBRARY_ID = ""
ZOTERO_LOCAL_DIR = ""
ZOTERO_LIBRARY_TYPE = "user"
ZOTERO_API_KEY = ""
SIOYEK_LOCAL_DATABASE_FILE_PATH = ""
SIOYEK_SHARED_DATABASE_FILE_PATH = ""
SIOYEK_PATH = ""
ZOTERO_TO_SIOYEK_COLORS = {
    "#5fb236": "g",
    "#a28ae5": "a",
    "#e56eee": "p",
    "#2ea8e5": "b",
    "#ff6666": "r",
    "#f19837": "o",
    "#ffd400": "y",
}

RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MGN = "\033[35m"
CYAN = "\033[36m"
RST = "\033[0m"

ConvertibleToNumbers = Union[str, bytes, int, float]


class ZoteroHighlight(NamedTuple):
    """Tuple class that store important information from zotero highlights and annotations."""

    text: str
    color: ConvertibleToNumbers
    page: int
    date_added: str
    date_modified: str
    abs_doc_page: int
    comment: str
    rects: list


class Document(TypedDict):
    """Sioyek document dictionary class."""

    id: int
    path: str
    hash: str


def calculate_md5(file_path):
    """

    Calculate a file md5sum hash.

    Parameters
    ----------
    file_path : str
        Complete file path

    Returns
    -------
    hash : str
        md5sum hash string of the file

    Examples
    --------
    >>> Path = __import__("pathlib").Path
    >>> current_script_path = Path(__file__).resolve()
    >>> two_folders_up = current_script_path.parents[2]
    >>> file_path = os.path.join(two_folders_up, "tests/E5M6X2IH/test.pdf")
    >>> print(calculate_md5(file_path))
    a52a77322278ecc41be7c43d233d4d17

    """
    md5_hash = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            md5_hash.update(chunk)
    return md5_hash.hexdigest()


# -TODO: Check annotationSortIndex value meaning
class ZoteroData:
    """

    A class to extract and store zotero highlight annotations from the user database.

    Class to handle highlight type annotations from zotero pdfs, being possible to specify
    the documents to manipulate based on the pdf file name or on the the highlight date of creation.

    Attributes
    ----------
    highlights : ZoteroHighlight
        list containing Highlight class elements, with the keys:
            text : str
                text of the highlight
            color : str
                html hex code
            page : str
                page number, considering the document as labeled in the document numeration
            date_added : str
                Addition of the highlight, formatted like %Y-%m-%d %H:%M:%S
            date_modified : str
                Addition of the highlight, formatted like %Y-%m-%d %H:%M:%S
            abs_doc_page : int
                Absolute page, starting in 1 always
            comment : str
                annotationComment / Comment text from the current highlight

    zotero_api : pyzotero.zotero.Zotero
        pyzotero class object, obtained from the user zotero database, from the given
        library id, library type, and api key

    last_modified_version : int
        Associates each item / collection with the last version (or greater) at which the item /
        collection was modified. Can be passed through the keyword arg since=versionNum, to
        retrieve only items / collections which have been modified since versionNum.


    Methods
    -------
    get_main_item(doc_name_path_title:str) -> dict
        Get the information from a given PDF zotero item.

    get_first_page_number(item:dict) -> int
        Get the relative first page from the document, as it is labeled in the PDF.

    extract_highlights(file_path:str)
        Update the class highlights attribute, with the obtained highlights from the file path.

    get_highlights_by_date(date:datetime.datetime, limit_inp:int, sort_inpt:str) -> dict
        Same from above Method, but instead of inputting the file_name string, takes a date, and
        queryes all the files more recent than the given date.

    print_get_highlights(file_path:str, sioyek_data:SioyekData)
        Prints to terminal the obtained formatted obtained highlights from the zotero item

    get_zotero_tags_by_pdf_path(file_path:str) -> str
        Get a zotero local PDF attachment parent item tags.

    add_zotero_tag_by_pdf_path(file_path:str, added_tag:str)
        Add a tag to a zotero PDF file attachment parent item.

    remove_zotero_tag_by_pdf_path(file_path:str, removed_tag:str)
        Remove a tag from a zotero PDF file attachment parent item.

    """

    zotero_api: zotero.Zotero
    highlights: list

    def __init__(
        self,
        zotero_api: Optional[zotero.Zotero] = None,
        library_id: Optional[str] = None,
        library_type: Optional[str] = None,
        api_key: Optional[str] = None,
        highlights: Optional[Sequence[ZoteroHighlight]] = None,
        annotations_data: Optional[list] = None,
        last_modified_version: Optional[int] = None,
        rects: Optional[int] = None,
    ):
        """

        Class ZoteroData initing.

        Parameters
        ----------
        zotero_api : zotero.Zotero, optional

        library_id : str, optional

        library_type : str, optional

        api_key : str, optional

        highlights : ZoteroHighlight, optional

        annotations_data : list, optional

        last_modified_version : int, optional

        """
        self.zotero_api = zotero.Zotero(library_id, library_type, api_key)
        self.highlights = []
        self.last_modified_version = self.zotero_api.last_modified_version()

    def get_local_pdf_path_by_title(self, item_title):
        """

        Get the local path to a zotero pdf item, given its title only.

        Parameters
        ----------
        item_title : str
            String with the PDF attachment title, may be the file or the zotero item title.

        Returns
        -------
        pdf_path : str
            Local path to the passed item.

        """
        options_parent = []
        options_title = []
        new_attach = self.zotero_api.items(q=item_title, itemtype="attachment")
        for n in new_attach:
            if "data" in n and "key" in n["data"]:
                new = self.zotero_api.children(n["data"]["key"])
                for a in new:
                    if "data" in a and "key" in a["data"]:
                        options_parent.append(a["data"]["key"])
                    if "data" in a and "parentItem" in a["data"]:
                        options_parent.append(a["data"]["parentItem"])
                    if "data" in a and "filename" in a["data"]:
                        options_title.append(a["data"]["filename"])
                    if "data" in a and "title" in a["data"]:
                        options_title.append(a["data"]["title"])
        for i in options_parent:
            new_path = ZOTERO_LOCAL_DIR + "/" + i
            if os.path.isdir(new_path):
                for k in options_title:
                    complete_path = os.path.abspath(new_path + "/" + k)
                    if os.path.isfile(complete_path):
                        return complete_path

    def get_main_item(self, doc_name_path_title):
        """

        Get a zotero item, given this item PDF attachment file name , path, or zotero item title.

        The following process order is adopted during the validation:

        First, checks if the parameter passed is an existing file, in case of positive testing
        checks for this file md5sum hash or for this local file complete path on the pyzotero user
        items, for confirmation that it is a file already in the database.

        Second, checks if the passed name is a zotero item title, by the use of the function
        get_local_pdf_path_by_title()

        Then checks for possiblity of being other zotero files fields descriptors, so tryes to
        query an item with more flexible adjustments than the first time, and also checks for
        matching files and folders on the user defined zotero local folder `ZOTERO_LOCAL_DIR`


        Parameters
        ----------
        doc_name_path_title : str
            Complete file path, File name, or Zotero item title.

        Returns
        -------
        new_item : dict
            Dictionary with all the pyzotero retrieved properties of the give zotero item main item

        """
        # If is an existing file, checks to match and confirm with the zotero database
        if os.path.exists(doc_name_path_title):
            md5_hash = calculate_md5(os.path.abspath(doc_name_path_title))
            name = os.path.basename(os.path.abspath(doc_name_path_title))
            items = self.zotero_api.items(q=name, itemtype="attachment")
            for item in items:
                for n in ["filename", "file_name", "name", "title"]:
                    if n in item["data"] and item["data"][n] == name:
                        new_item = self.zotero_api.item(item["data"]["parentItem"])
                        return new_item

                if "md5" in item["data"] and item["data"]["md5"] == md5_hash:
                    new_item = self.zotero_api.item(item["data"]["parentItem"])
                    return new_item
        # Title Checking
        else:
            local_path = self.get_local_pdf_path_by_title(doc_name_path_title)
            if local_path is not None:
                return local_path
        # Other unindentified zotero fields descriptors
        new_attach = self.zotero_api.items(q=doc_name_path_title, itemtype="attachment")
        if new_attach:
            for item in new_attach:
                if "data" in item and "parentItem" in item["data"]:
                    return item["data"]["parentItem"]
        else:
            items = self.zotero_api.items(q=doc_name_path_title)
            if isinstance(items, list) and len(items) > 0:
                return items[0]

        # Tryes to find matching resources on user defined zotero local folder
        for root, _, files in os.walk(ZOTERO_LOCAL_DIR):
            if doc_name_path_title in files:
                return os.path.join(root, doc_name_path_title)

        # In last case, try to get the name of a zotero item based on the folder of the PDF,
        # Automatic schema of zotero stores local PDFs in folders containing the item key identifier
        parent_name = os.path.basename(os.path.dirname(doc_name_path_title))
        if re.match(r"^[A-Z0-9]+$", parent_name):
            new_item = self.zotero_api.item(parent_name)
            parent_key = new_item["data"]["parentItem"]
            new_item = self.zotero_api.item(parent_key)
            return new_item

        else:
            raise ValueError
            print("Error!, the passed parameter don't match a pdf file from zotero")

        return None

    def get_first_page_number(self, item):
        """

        Calculate the relative first page number of a given Zotero item.

        Parameters
        ----------
        item : dict
            Pyzotero retrieved item data

        Returns
        -------
        absolute_page_number : int
            Document absolute page number, starting in 1

        Notes
        -----
        Zotero attachment PDF page retrieved by pyzotero, is the page as it is numbered in the PDF,
        like if it is a book chapter from pages 750-760, it considers the first page has the number
        750, but since sioyek considers the page starts necessary in 0, its necessary to convert
        the page number in this cases.

        """
        first_page = item["data"].get("pages")
        if first_page is None:
            item = self.zotero_api.item(item["data"]["parentItem"])
        first_page = item["data"].get("pages")
        first_part = first_page.split("-")[0]
        first_part_match = bool(re.fullmatch(r"\d+", first_part))
        if first_page is not None and first_part_match and int(first_part) > 0:
            return int(first_part)
        return 1

    def extract_highlights(self, file_name_or_path):
        """

        Given a zotero item key, extract it highlights.

        Parameters
        ----------
        item_key : str
            str of a zotero item key

        Notes
        -----
        This function extracts the higlights to the class lists highlights.

        """
        exists = os.path.isfile(file_name_or_path)
        if not exists:
            file_name_or_path = self.get_local_pdf_path_by_title(file_name_or_path)
        item = self.get_main_item(file_name_or_path)
        first_page = self.get_first_page_number(item)
        children_items = self.zotero_api.children(item["key"])
        for n in children_items:
            annotations = self.zotero_api.children(n["key"], itemtype="annotation")
            if annotations:
                break

        for annotation in annotations:
            if annotation["data"]["annotationType"] == "highlight":
                text = annotation["data"].get("annotationText", "")
                color = annotation["data"].get("annotationColor", "")
                page = annotation["data"].get("annotationPageLabel", "")
                date_added = annotation["data"].get("dateAdded", "")
                date_modified = annotation["data"].get("dateModified", "")
                abs_doc_page = int(page) - (int(first_page) - 1)
                comment = annotation["data"].get("annotationComment", "")
                rects = annotation["data"].get("annotationPosition", "")
                if abs_doc_page <= 0:
                    abs_doc_page = int(page)
                highlight = ZoteroHighlight(
                    text,
                    color,
                    page,
                    date_added,
                    date_modified,
                    abs_doc_page,
                    comment,
                    rects,
                )
                self.highlights.append(highlight)

    def get_highlights_by_date(self, date=None, limit_inp=10, sort_inp="dateAdded"):
        """

        Given a date, return all zotero highlights made after that.

        Parameters
        ----------
        date : datetime.datetime (default First day of current year)
            Date to filter highlights to start at

        limit_inp : int (default 10)
            Max number of items to retrieve from the zotero database

        sort_inp : str (default dateAdded)
            Sorting method of the zotero items, can be one of the following:
                dateAdded,
                dateModified,
                title,
                creator,
                type,
                date,
                publisher,
                publicationTitle,
                journalAbbreviation,
                language,
                accessDate,
                libraryCatalog,
                callNumber,
                rights,
                addedBy,
                numItems,
                tags

        Returns
        -------
        None

        """
        if date is None:
            date = datetime.datetime(datetime.datetime.today().year - 1, 1, 1)

        if type(date) is str:
            date = datetime.datetime.strptime(date, "(%Y, %m, %d)")

        date_str = date.strftime("%Y-%m-%dT%H:%M:%SZ")

        items = self.zotero_api.items(
            last_modified=date_str,
            sort=sort_inp,
            limit=limit_inp,
            itemType="attachment",
        )

        date_highlights = {}

        for item in items:
            if "parentItem" in item["data"]:
                self.extract_highlights(item["data"]["key"])
                date_highlights[item["data"]["parentItem"]] = self.highlights

        return date_highlights

    def print_get_highlights(self, file_path, sioyek_data):
        """

        Print highlights retrieved from a local PDF present in zotero database.

        Parameters
        ----------
        file_path : str
            Path to a local PDF file, present in the zotero database.

        sioyek_data : SioyekData
            Sioyek highlights class

        Returns
        -------
        None

        """
        self.extract_highlights(clean_path(file_path))
        highlights = self.highlights
        n = 1
        print("\n")
        for highlight in highlights:
            mod_date = sioyek_data.convert_zot_date_to_sioyek(highlight.date_modified)
            create_date = sioyek_data.convert_zot_date_to_sioyek(highlight.date_added)
            colored_color = print_colored_string(highlight.color, highlight.color, auto_print=False)
            print(
                textwrap.dedent(
                    f"""\
                {print_colored_string(n, highlight.color, auto_print=False)}
                {print_colored_string("-----", highlight.color, auto_print=False)}
                Text: {highlight.text}
                Color: {colored_color}
                Relative Page: {highlight.page}
                Doc Page: {highlight.abs_doc_page}
                Creation Date: {create_date}
                Modification Date: {mod_date}
                Rects: {highlight.rects}
                """
                )
            )
            n += 1

    def get_zotero_tags_by_pdf_path(self, file_path):
        """

        Get a zotero local PDF attachment parent item tags.

        Parameters
        ----------
        pdf_path : str
            Local complete PDF file path.

        Returns
        -------
        tags_str : str
            Zotero item tags, separated by ','

        """
        item = self.get_main_item(file_path)
        tags_list = []
        for n in item["data"]["tags"]:
            tags_list.append(n["tag"])

        return ", ".join(tags_list)

    def add_zotero_tag_by_pdf_path(self, file_path, added_tag):
        """

        Add a tag to a zotero PDF file attachment parent item.

        Parameters
        ----------
        file_path : str
            Complete local file path to PDF file attachment present in zotero.

        added_tag : str
            Tag name to add to the zotero item.

        Returns
        -------
        None

        """
        item = self.get_main_item(file_path)
        if {"tag": added_tag} in item["data"]["tags"]:
            print(f"Tag {RED}{added_tag}{RST} Already exists in PDF parent item!")
            return
        else:
            item["data"]["tags"].append({"tag": added_tag})
            self.zotero_api.update_item(item)
            print(f"Tag {CYAN}{added_tag}{RST} added to PDF parent item.")
            return
        print(f"{RED}Given PDF file md5 hash not found in Zotero attachments!{RST}")
        return

    def remove_zotero_tag_by_pdf_path(self, file_path, removed_tag):
        """

        Remove a tag from a zotero PDF file attachment parent item.

        Parameters
        ----------
        file_path : str
            Complete local file path to PDF file attachment present in zotero.

        removed_tag : str
            Tag name to remove from the zotero item.

        Returns
        -------
        None

        """
        item = self.get_main_item(file_path)
        if {"tag": removed_tag} in item["data"]["tags"]:
            item["data"]["tags"].remove({"tag": removed_tag})
            self.zotero_api.update_item(item)
            print(f"Tag {CYAN}{removed_tag}{RST} removed from item.")
            return
        else:
            print(f"Tag {RED}{removed_tag}{RST} not found in the given PDF parent item!")
            return

    def get_pdf_cite_key(self, file_path):
        """

        Print the extra data from the parent of a local PDF file.

        Parametters
        -----------
        file_path : str
            local PDF file path.

        """
        item = self.get_main_item(file_path)
        if re.match(r"^Citation Key:", item["data"]["extra"]).group():
            return re.sub(r"^Citation Key:\s*", "", item["data"]["extra"])

        return item["data"]["extra"]


class SioyekData:
    """

    Sioyek highligts class.

    Attributes
    ----------
    local_database_file_path : str
        Path to the local database .db file path

    shared_database_file_path : str
        Path to the shared database .db file path

    sioyek_path : str
        Path to the sioyek executable

    zotero_hl_to_sioyek : dict
        Dictionary wich keys are zotero highlight html colors, and the value is the sioyek
        highlight letter, to which this highlights should be when embedding in sioyek

    docs : list
        list of dicts, containing the documents in the sioyek database, having each dict the id
        of a file, the path to this file, and the hash to this file path, for example:

    sioyek : sioyek.sioyek.Sioyek
        Sioyek python class object, to execute sioyek commands

    Methods
    -------
    list_files()
        List all file paths and hashes in the sioyek database

    list_hash(file:str)
        Given a file, print this file hash

    get_attributes(file:str) -> dict
        Return a dict with the highlights data fields.

    is_string_in_dicts(string:str, list_of_dicts:list) -> bool
        Checks in a list of dicts for any dict value matching a given string, returning a boolean.

    insert_documents(file_path:str)
        Insert if don't exist, a file into local sioyek database.

    print_attributes(file:str)
        Print all attributes from sioyek database file, and this attributes values.
        the attributes are bookmarks, highlights, links and marks.

    to_abs(highlights:ZoteroData.highlights, file_path:str) -> tuple
        Get the absolute position of a document highlight, based on the highlight text, the
        highlight page, and the document file path.

    convert_zot_date_to_sioyek(date_str:str) -> str
        Convert a date from zotero default format to sioyek format.

    get_zotero_to_sioyek_data(file_path:str,
                                     zotero_data:__main__.ZoteroData) -> list
        Get a zotero file highlights, formatted in a dict with essential data to embed to sioyek.

    insert_highlight(file_path:str, zotero_data:__main__.ZoteroData)
        Insert a zotero file annotations to this sioyek file database.

    Examples
    --------
    docs attribute example of list:
    [{'id': 1,
      'path': '/home/user/Zotero/storage/RZ54E2RK/processing_of_calcium_sulfate_the_.pdf',
      'hash': '04456fccdb9854ca3bea51d6442d9bb2',
     },
     {'id': 2,
      'path': '/home/user/Programação/LaTeX/tutorial/tut.pdf',
      'hash': '4e35e5dca3a3f648ba6594453347f498',
     },
     {'id': 3,
      'path': '/home/user/Library/python/numpydoc.pdf',
      'hash': '82f60ed6cc8e494a82d24d84105065b0',
     }
    ]
    """

    # -PERF: Change the load method of docs variable, since it can be a relly big element, being
    #  loaded at class initing. Some of the usages of the docs variable can be modified to other
    #  methods too.
    def __init__(
        self,
        local_database_file_path: Optional[str] = None,
        shared_database_file_path: Optional[str] = None,
        sioyek_path: Optional[str] = None,
        zotero_hl_to_sioyek: Optional[dict] = None,
        docs: Optional[Sequence[Document]] = None,
        sioyek: Optional[Sioyek] = None,
        local_db: Optional[sqlite3.Connection] = None,
        shared_db: Optional[sqlite3.Connection] = None,
        highlight_embed_method="custom",
        force_binary=False,
    ):
        """

        Class SioyekData highlights initing.

        Parameters
        ----------
        local_database_file_path : str, optional

        shared_database_file_path : str, optional

        sioyek_path : str, optional

        zotero_hl_to_sioyek : str, optional

        docs : Sequence[Document], optional

        sioyek : Sioyek, optional

        local_db : sqlite3.Connection, optional

        shared_db : sqlite3.Connection, optional

        highlight_embed_method : str, default: custom

        force_binary : bool, default: False

        """
        check_env_variables()
        self.zotero_hl_to_sioyek = ZOTERO_TO_SIOYEK_COLORS
        if local_database_file_path is not None and shared_database_file_path is not None:
            self.local_db = sqlite3.connect(clean_path(local_database_file_path))
            self.shared_db = sqlite3.connect(clean_path(shared_database_file_path))
            local_cursor = self.local_db.cursor()
            local_cursor.execute("select * from document_hash")
            documents = local_cursor.fetchall()
            column_names = [description[0] for description in local_cursor.description]
            self.docs = [dict(zip(column_names, bm)) for bm in documents]
            self.sioyek = Sioyek(
                clean_path(sioyek_path),
                clean_path(local_database_file_path),
                clean_path(shared_database_file_path),
            )
            self.doc = None
        else:
            self.sioyek = None

    def list_files(self):
        """List all file paths and hashes in the sioyek database."""
        for doc in self.docs:
            print(doc["hash"], ":", doc["path"])

    def list_hash(self, file):
        """

        Given a file, prints this file hash.

        Parameters
        ----------
        file : str

        Returns
        -------
        None

        """
        found = False
        for doc in self.docs:
            if pathlib.Path(doc["path"]).samefile(file):
                print(doc["hash"])
                found = True
                break
        if not found:
            print("File not found in the database.")

    def get_attributes(self, file_path):
        """

        Return a dict with the highlights data fields.

        Parameters
        ----------
        file_path : str
            String of a file path.

        Returns
        -------
        from_annotation : dict
            dict with the keys:
                bookmarks : list
                highlights : list
                    list of dicts, with the keys:
                        id : int
                            number of the highlight index
                        document_path : str
                            hash str of the document path
                        desc : str
                            text of the highlight
                        text_annot : str
                            annotation of the highlight
                        type : str
                            letter of the sioyek highlight type
                        creation_time : str
                            date formatted like %Y-%m-%d %H:%M:%S
                        modification_time : str
                            date formatted like %Y-%m-%d %H:%M:%S
                        uuid : str
                            uuid of the highlight
                        begin_x : float
                            coordinate of the sioyek absolute position x begin
                        begin_y : float
                            coordinate of the sioyek absolute position y begin
                        end_x : float
                            coordinate of the sioyek absolute position x end
                        end_y : float
                            coordinate of the sioyek absolute position y end

        Examples
        --------
        An example of a returned from_annotations dict:
        {'bookmarks': [],
         'highlights': [{'id': 1,
                         'document_path': '04456fccdb9854ca3bea51d6442d9bb2',
                         'desc': 'thermodynamic databases.',
                         'text_annot': 'None',
                         'type': 'i', 'creation_time': '2024-08-13 15:53:45',
                         'modification_time': '2024-08-13 15:53:45',
                         'uuid': '0b573e66-66aa-4fc7-886b-2e21d94104af',
                         'begin_x': -198.7873992919922, 'begin_y': 1121.375,
                         'end_x': -156.77529907226562, 'end_y': 1155.4794921875}],
         'links': [],
         'marks': []}

        """
        table_names = [
            ("bookmarks", "document_path"),
            ("highlights", "document_path"),
            ("links", "src_document"),
            ("marks", "document_path"),
        ]
        from_annotations = {}
        from_hash = calculate_md5(file_path)
        for table, column_name in table_names:
            with self.shared_db as conn:
                cursor = conn.cursor()
                cursor.execute(f"SELECT * FROM {table} WHERE {column_name} = ?", (from_hash,))
                annotations = cursor.fetchall()
                column_names = [description[0] for description in cursor.description]
                from_annotations[table] = [dict(zip(column_names, bm)) for bm in annotations]
        return from_annotations

    def undo_last(self):
        """

        Undo last insert highlight on sioyek database operation.

        Parameters
        ----------
        None

        Raises
        ------
        FileNotFoundError
            If the file does not exist.

        """
        try:
            with open("/tmp/zot2sioyek/last_highlights_uuids") as file:
                lines = file.readlines()
                lines = [line.strip() for line in lines]
        except FileNotFoundError:
            print("Error: The file /tmp/zot2sioyek/last_highlights_uuids does not exist.")
            raise
        with self.shared_db as conn:
            cursor = conn.cursor()
            query = "delete from highlights where uuid = ?"
            for n in lines:
                cursor.execute(query, (n,))
                conn.commit()

    def delete_highlights(self, file_path):
        """

        Delete all highlights from a sioyek database file.

        Parameters
        ----------
        file_path : str
            Complete file path, file name if present in zotero local folder, or zotero item title.

        """
        from_hash = calculate_md5(file_path)
        with self.shared_db as conn:
            cursor = conn.cursor()
            query = "delete from highlights where document_path = ?"
            cursor.execute(query, (from_hash,))
            conn.commit()
        print(f"Deleted highlights from {file_path}")

    def is_string_in_dicts(self, string, list_of_dicts):
        """

        Check if a given string matches any dict value from a list of dicts.

        Parameters
        ----------
        string : str
            String to search for matches in the dicts values

        list_of_dicts : list
            List, with each element being a dict, being this dicts the ones that will
            have the values checked for matchings with the given string.

        Returns
        -------
        bool
            Boolean, True if any value of the dicts mathces the string, and False if not.

        """
        for dictionary in list_of_dicts:
            if any(string in str(value) for value in dictionary.values()):
                return True
        return False

    def insert_document(self, file_path):
        """

        Check and insert a file if don't exist in local sioyek database.

        Parameters
        ----------
        file_path : str
            Complete file path

        """
        # local_db = sqlite3.connect(clean_path(self.local_database_file_path))
        md5_hash = calculate_md5(file_path)
        doc_exists = self.is_string_in_dicts(md5_hash, self.docs)
        user_inp = None
        q_doc_insert = None
        if not doc_exists:
            q_doc_insert = f"""
            INSERT INTO document_hash(path, hash)
            VALUES ('{file_path}','{md5_hash}');
            """
            file_name = f"{path.basename(clean_path(file_path))}"
            user_inp = input(
                textwrap.dedent(
                    f"""\
                Insert {CYAN}{file_name}{RST} in {MGN}local Sioyek database{RST}? {BLUE}(y/n){RST}:
            """
                )
            )
        if user_inp in ["Y", "y", "yes"]:
            if q_doc_insert is not None:
                print(q_doc_insert)
            print(f"{file_name} {GREEN} Added to local database{RST}")
            self.local_db.execute(q_doc_insert)
            self.local_db.execute("commit")
        elif user_inp in ["N", "n", "no"]:
            print(f"{file_name} {RED}Addition abortted!{RST}")
        elif user_inp is not None:
            print(f"{RED}Answer should be y or n!{RST}")

    def print_attributes(self, file_path):
        """

        Print all attributes from sioyek database file, and this attributes values.

        the attributes are bookmarks, highlights, links and marks.

        Parameters
        ----------
        file_path : str
            String of a file path.

        Returns
        -------
        None

        """
        from_annotations = self.get_attributes(file_path)
        colors_list = [f"{CYAN}", f"{MGN}", f"{YELLOW}", f"{GREEN}"]
        for key, attribute in from_annotations.items():
            idx = list(from_annotations).index(key)
            print(f"{colors_list[idx]}{key}\n{'=' * len(key)}{RST}\n")
            for idx, value in enumerate(attribute):
                print(f"{idx + 1}\n--------")
                for i, j in value.items():
                    print(f"{i}: {j}")
            print("\n")

    def zotero_rects_to_abs(self, file_path, highlight):
        """

        Zotero highlight importing, using the highlight coordinates obtained from the zotero itself.

        Parameters
        ----------
        file_path : str
            Local PDF to import the highlights from zotero to sioyek

        highlight : ZoteroData.highlights
            Zotero class for handling annotations and highlights

        Returns
        -------
        rects : list
            List of Absolute document positions from the beginning and enging of each highlight.

        """
        rects = json.loads(highlight.rects)
        self.doc = self.sioyek.get_document(file_path)
        print(rects)
        curr_page = rects["pageIndex"]
        offset_x = self.doc.page_widths[curr_page] / 2
        offset_y = self.doc.cum_page_heights[curr_page]
        rects_new = [
            fitz.Rect(
                round(float(n[0]) - offset_x, 4),
                round(float(n[1]) + offset_y, 4),
                round(float(n[2]) - offset_x, 4),
                round(float(n[3]) + offset_y, 4),
            )
            for n in rects["rects"]
        ]

        return rects_new

    def calculate_match_score(self, extracted_string, reference_string):
        """

        Calculate the match score bwtween two strings.

        Parameters
        ----------
        extracted_string : str
            The string to get the matching score

        reference_string : str
            Fixed string, that corresponds to a perfect math = 1, to which reference str will be
            compared

        Returns
        -------
        float
            Matching score, ranging 0 to 1

        Examples
        --------
        >>> test_match = SioyekData().calculate_match_score(
        ...     "test extracted string to check", "test reference string to check"
        ... )
        >>> print(test_match)
        0.7

        """
        return sum(1 for a, b in zip(extracted_string, reference_string) if a == b) / max(
            len(reference_string), len(extracted_string)
        )

    def modify_rectangle(self, rect, axis, position, final, step_size=0.5):
        """

        Modify a given pymupdf rectangle, in a defined order to try to find a more appropriate rect.

        Parameters
        ----------
        rect : pymupdf.Rect
            pymupdf rectangle, with elements x0, y0, x1, y1
        axis : str
            string matching "x" or "y", defining which elements should be varied
        position : str
            string matchong "begin" or "end", defining which elements should be varied (begin match
            x0 and y0, end match x1 and y1)
        final : bool
            Boolean to mark the last modify operation, trying one last possibility
        step_size : float, default 1
            Total delta variation on the rect element

        Returns
        -------
        pymupdf.Rect
            pymupdf rectangle, with elements x0, y0, x1, y1

        """
        axis : str
        x0, y0, x1, y1 = rect
        if final == 1:
            return fitz.Rect(x0, y0, x1, y0)
        if final == 2:
            return fitz.Rect(x1, y0, x0, y1)
        if axis == "y":
            delta_x = 0
            delta_y = step_size
        if axis == "x":
            delta_y = 0
            delta_x = step_size
        if position == "begin":
            return fitz.Rect(x0 + delta_x, y0 + delta_y, x1, y1)
        elif position == "end":
            return fitz.Rect(x0, y0, x1 - delta_x, y1 - delta_y)

    def extract_string_from_pdf(self, abs_rect):
        """

        Extract the string from a given pdf rect.

        Parameters
        ----------
        abs_rect : pymupdf.Rect
            Pymupdf rect, containing x0, y0, x1 and y1

        Returns
        -------
        result : str
            Obtained string from given rectangle

        """
        str_list = []
        selection_begin_abs = AbsoluteDocumentPos(abs_rect.x0, abs_rect.y0)
        selection_end_abs = AbsoluteDocumentPos(abs_rect.x1, abs_rect.y1)
        selected_words = self.doc.get_selected_words(selection_begin_abs, selection_end_abs)
        for n in selected_words[0]:
            str_list.append(n[4])
        result = " ".join(str_list)
        return result

    def optimize_coordinates(
        self, initial_rect, reference_string, max_iterations=100, tolerance=0.90
    ):
        """

        Optimize a pdf highlight rectangle, based on the text it should have and the actual text.

        Parameters
        ----------
        initial_rect : pymupdf.Rect
            Pymupdf rectange with the elements x0, y0, x1 and y1
        reference_string : str
            String the highlight should contain
        max_iterations : int, default 4000
            The maximum number of iterations on the coordinate elements of the rectangle
        tolerance : float, default 0.98
            The matching between reference string and actual string to consider that they are the
            same and return the results withou going over all the maximum iterations

        Returns
        -------
        best_rect : pymupdf.Rect
            Pymupdf rectange with the elements x0, y0, x1 and y1
        best_score : float
            Matching from the best rectangle, ranging 0 to 1
        extracted_string : str
            String obtained from the best_rect, using pymupdf
        """
        rect = initial_rect
        best_score = 0
        last_score = 0
        best_rect = rect
        axis = "y"
        last_rect = rect
        position = "begin"
        final = 0
        for _ in range(max_iterations):
            extracted_string = self.extract_string_from_pdf(rect)
            match_score = self.calculate_match_score(extracted_string, reference_string)
            if match_score > best_score:
                best_score = match_score
                best_rect = fitz.Rect(tuple(round(x, 4) for x in rect))

            if match_score >= tolerance:
                break

            if match_score < last_score:
                rect = last_rect
                if final == 2:
                    break
                if final == 1:
                    final = 2
                if axis == "y" and position == "begin":
                    position = "end"
                elif axis == "y" and position == "end":
                    axis = "x"
                    position = "begin"
                elif axis == "x" and position == "begin":
                    position = "end"
                elif axis == "x" and position == "end":
                    final = 1
            last_rect = rect
            rect = self.modify_rectangle(rect, axis, position, final)
            last_score = match_score

        return best_rect, best_score, extracted_string

    def to_abs(self, file_path, highlight):
        """

        Get the absolute position of a document highlight, based on the text, page and file path.

        Parameters
        ----------
        file_path : str
            String of a file path

        highlight : ZoteroData.highlight
            Zotero highlights class object

        Returns
        -------
        best_rect : tuple
            Two tuples containing two elements each, being the first the absolute position of the
            starting offset x and y, and the other the absolute position to the endings ofthem.

        """
        rects = []
        curr_page = highlight.abs_doc_page - 1
        self.doc = self.sioyek.get_document(file_path)
        rects = self.doc.get_best_selection_rects(curr_page, highlight.text, merge=False)
        offset_x = self.doc.page_widths[curr_page] / 2
        offset_y = self.doc.cum_page_heights[curr_page]
        rects = [
            fitz.Rect(
                round(n[0] - offset_x, 4),
                round(n[1] + offset_y, 4),
                round(n[2] - offset_x, 4),
                round(n[3] + offset_y, 4),
            )
            for n in rects
        ]
        try:
            if len(rects) > 1:
                rect = fitz.Rect(
                    rects[0].x0,
                    rects[0].y0,
                    rects[-1].x1,
                    rects[-1].y1,
                )
            else:
                rect = rects[0]
        except ValueError:
            print("Highlight boxes identification by text failed.")
            return None
        best_rect, best_score, extracted_string = self.optimize_coordinates(rect, highlight.text)
        return best_rect, best_score, extracted_string

    def convert_zot_date_to_sioyek(self, date_str):
        """

        Convert a date from zotero default format to sioyek format.

        Parameters
        ----------
        date_str : str
            date string in zotero default format, '%y-%m-%dt%h:%m:%sz'

        Returns
        -------
        formatted_date_str : str
            date string in sioyek default format, '%y-%m-%d %h:%m:%s'

        Examples
        --------
        >>> time_test = SioyekData().convert_zot_date_to_sioyek("2024-08-13t15:53:45z")
        >>> print(time_test)
        2024-08-13 15:53:45

        """
        date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
        formatted_date_str = date_obj.strftime("%Y-%m-%d %H:%M:%S")
        return formatted_date_str

    def get_zotero_to_sioyek_data(self, file_path, zotero_data, method="custom", flags=0):
        """

        Get a zotero file highlights, formatted in a dict with essential data to embed to sioyek.

        Parameters
        ----------
        file_path : str
            complete file path

        zotero_data : __main__.zoterodata
            main zotero highlights class

        method : str, default 'custom'
            Highlighting method that should be used, can be `custom`, which implements sioyek native
            type of highlighting, `fitz`, that implements the pymupdf type of highlighting with each
            unique options and customization, and last `zotero`, which uses the zotero highlights
            rectangles instead of calculating again.

        flags : int, defaults 0
            Fitz specific flags options for defining how to handle text elements:
                FZ_STEXT_PRESERVE_LIGATURES = 1,
                FZ_STEXT_PRESERVE_WHITESPACE = 2,
                FZ_STEXT_PRESERVE_IMAGES = 4,
                FZ_STEXT_INHIBIT_SPACES = 8,
                FZ_STEXT_DEHYPHENATE = 16,
                FZ_STEXT_PRESERVE_SPANS = 32,
                FZ_STEXT_MEDIABOX_CLIP = 64,

        Returns
        -------
        zotero_annotations : list
            list containing highlight dicts, being one dict per highlight

        Examples
        --------
        zotero_annotations example list of dict:
        [{'document_path': '04456fccdb9854ca3bea51d6442d9bb2',
          'desc': 'thermodynamic databases.,
          'type': 'i', 'begin_x': '-198.7873992919922',
          'begin_y': '1121.375', 'end_x': '-156.77529907226562', 'end_y': '1155.4794921875',
          'text_annot': 'none', 'creation_time': '2024-08-13 15:53:45',
          'modification_time': '2024-08-13 15:53:45',
          'uuid': 'cc3366af-b523-4a67-a802-c7afd846d942',
          'page': 335
          'absolute_page': 1
         },
         {'document_path': '04456fccdb9854ca3bea51d6442d9bb2',
          'desc': 'reported by many authors and used in practice for several decades,',
          'type': 'd', 'begin_x': '-165.0081024169922', 'begin_y': '997.185546875',
          'end_x': '-152.75357055664062', 'end_y': '1031.2900390625',
          'text_annot': 'none', 'creation_time': '2024-08-13 15:53:42',
          'modification_time': '2024-08-13 15:53:42',
          'uuid': '58d238b6-1b42-4b52-97aa-4773b9b6c734',
          'page': 335
          'absolute_page': 1
          }]


        See Also
        --------
        fitz : util.c
            Fitz byte flags options definitions


        """
        threshold = 0.90
        zotero_data.extract_highlights(file_path)
        highlights = zotero_data.highlights
        zotero_annotations = []
        for highlight in highlights:
            if method == "custom":
                abs_rect, _, _ = self.to_abs(file_path, highlight)
            elif method == "zotero":
                abs_rect = self.zotero_rects_to_abs(file_path, highlight)
            zotero_annotations.append({
                "document_path": calculate_md5(file_path),
                "desc": highlight.text,
                "type": self.zotero_hl_to_sioyek[highlight.color],
                "begin_x": str(abs_rect.x0),
                "begin_y": str(abs_rect.y0),
                "end_x": str(abs_rect.x1),
                "end_y": str(abs_rect.y1),
                "text_annot": highlight.comment,
                "creation_time": self.convert_zot_date_to_sioyek(highlight.date_added),
                "modification_time": self.convert_zot_date_to_sioyek(highlight.date_modified),
                "uuid": str(uuid.uuid4()),
                "page": highlight.page,
                "absolute_page": highlight.abs_doc_page,
            })
        for i in range(len(highlights)):
            for j in range(i + 1, len(highlights)):
                ratio = SequenceMatcher(None, highlights[i].text, highlights[j].text).ratio()
                if ratio >= threshold:
                    zotero_annotations.remove(zotero_annotations[i])

        return zotero_annotations

    def list_all_sioyek_highlights(self):
        """

        Get all sioyek database documents highlights, and list them.

        Parameters
        ----------
        None

        Returns
        -------
        None

        """
        cursor = self.shared_db.cursor()
        cursor.execute("select * from highlights")
        documents = cursor.fetchall()
        for n in documents:
            print(
                textwrap.dedent(
                    f"""\
            {n[0]}
            -----
            id: {n[0]}
            document path md5: {n[1]}
            text: {n[2]}
            annotation: {n[3]}
            type: {n[4]}
            creation: {n[5]}
            modification: {n[6]}
            highligh uuid: {n[7]}
            begin x: {n[8]}
            begin y: {n[9]}
            end x: {n[10]}
            end y: {n[11]}
            """
                )
            )

    def write_list_to_file(self, file_path, data_list):
        """

        Write each element from a list in a local file.

        Parameters
        ----------
        file_path : str
            The path of the file to check or create.
        data_list : list
            The list of elements to write to the file, one element per line.

        Notes
        -----
        - If the file exists and is not empty, the file is cleared (made blank) before writing.
        - If the file does not exist, it will be created.
        - If the file's directory does not exist, it will be created.

        Examples
        --------
        Creating a file and writing list elements to its lines
        >>> SioyekData().write_list_to_file("tests/example.txt", ["item1", "item2", "item3"])
        File 'tests/example.txt' did not exist and has been created.

        Reading the written file
        >>> with open("tests/example.txt") as file:
        ...     lines = file.readlines()
        ...     lines = [line.strip() for line in lines]
        >>> print(lines)
        ['item1', 'item2', 'item3']

        Removing the created file
        >>> subprocess.run(["rm", "-rf", "tests/example.txt"])
        CompletedProcess(args=['rm', '-rf', 'tests/example.txt'], returncode=0)

        """
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Directory '{directory}' did not exist and has been created.")
        if os.path.exists(file_path):
            if os.path.getsize(file_path) > 0:
                with open(file_path, "w") as file:
                    pass
                print(f"File '{file_path}' was not blank and has been cleared.")
            else:
                print(f"File '{file_path}' already exists and is blank.")
        else:
            open(file_path, "w").close()
            print(f"File '{file_path}' did not exist and has been created.")

        with open(file_path, "w") as file:
            for item in data_list:
                file.write(f"{item}\n")

    def insert_highlight(self, file_path, zotero_data, method="custom", flags=2):
        """

        Insert a zotero file annotations to this sioyek file database.

        inser a zotero file highlights into a sioyek file, through sqlite3.
        the colors association is based on the color dict of the start of this file, and the
        function checks for repeated annotations through both databases, to not insert repeated
        highlights. repeated highlights is checked through the highligh similarity, if above
        90%.
        when a highlight is inserted in the sioyek file, it also prints the execed sqlite3 command.

        Parameters
        ----------
        file_path : str
            complete file path present in zotero and sioyek database

        zotero_data : __main__.zoterodata
            zoterodata class

        method : str, default 'custom'
            Highlighting method that should be used, can be `custom`, which implements sioyek native
            type of highlighting, `fitz`, that implements the pymupdf type of highlighting with each
            unique options and customization, and last `zotero`, which uses the zotero highlights
            rectangles instead of calculating again.


        flags : int, defaults 0
            Fitz specific flags options for defining how to handle text elements:
                FZ_STEXT_PRESERVE_LIGATURES = 1,
                FZ_STEXT_PRESERVE_WHITESPACE = 2,
                FZ_STEXT_PRESERVE_IMAGES = 4,
                FZ_STEXT_INHIBIT_SPACES = 8,
                FZ_STEXT_DEHYPHENATE = 16,
                FZ_STEXT_PRESERVE_SPANS = 32,
                FZ_STEXT_MEDIABOX_CLIP = 64,

        Notes
        -----
        the only field not present in the inserted highlight is the highlight id number, this way
        it permits to add highlights to files that already contain sioyek highlights, and the id
        number is automatically generated by sioyek.


        See Also
        --------
        fitz : util.c
            Fitz byte flags options definitions

        """
        last_uuid_list = []
        if self.sioyek.connected:
            subprocess.run([
                clean_path(SIOYEK_PATH),
                "--execute-command",
                "set_status_string",
                "--execute-command-data",
                "Importing Zotero Highlights...",
            ])
        if not os.path.isfile(file_path):
            file_path = zotero_data.get_local_pdf_path_by_title(file_path)
        self.insert_document(file_path)
        tables = self.get_zotero_to_sioyek_data(file_path, zotero_data, method=method)
        from_annotations = self.get_attributes(file_path)
        tables_to_keep = [
            table
            for table in tables
            if not any(
                SequenceMatcher(None, table["desc"], annotation["desc"]).ratio() >= 0.98
                for annotation in from_annotations["highlights"]
            )
        ]
        for table in tables_to_keep:
            q_hi_insert = """
            INSERT INTO highlights (
                document_path,
                desc,
                type,
                begin_x,
                begin_y,
                end_x,
                end_y,
                text_annot,
                creation_time,
                modification_time,
                uuid
            )
            VALUES (
                '{}', '{}', '{}', {}, {}, {}, {}, '{}', '{}', '{}', '{}'
            );
            """.format(
                table["document_path"],
                table["desc"],
                table["type"],
                table["begin_x"],
                table["begin_y"],
                table["end_x"],
                table["end_y"],
                table["text_annot"],
                table["creation_time"],
                table["modification_time"],
                table["uuid"],
            )
            last_uuid_list.append(table["uuid"])
            print(q_hi_insert)
            self.shared_db.execute(q_hi_insert)
            self.shared_db.execute("commit")
        self.write_list_to_file("/tmp/zot2sioyek/last_highlights_uuids", last_uuid_list)
        if self.sioyek.connected:
            subprocess.run([
                clean_path(SIOYEK_PATH),
                "--execute-command",
                "set_status_string",
                "--execute-command-data",
                f"{len(tables_to_keep)} Zotero Highlights Imported",
            ])
            self.sioyek.reload()


def hex_to_rgb(hex_color):
    """

    Convert a html hex to rgb.

    Parameters
    ----------
    hex_color : str
        Html hex color code

    Returns
    -------
    rgb : tuple
        r,g,b tuple, rangin each color from 0 to 255

    Examples
    --------
    >>> rgb = hex_to_rgb("#ff6666")
    >>> print(rgb)
    (255, 102, 102)

    """
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))


def print_colored_string(string, hex_color, auto_print=True):
    """

    Print to terminal a string colored with a html hex code color.

    Parameters
    ----------
    string : str
        string to be printted

    hex_color : str
        html hex code color

    auto_print : bool
        Whether to print the colored string, or to return the string ansi escaped.

    Returns
    -------
    str
        Ansi escaped string, with the correct color, returned only if auto_print=False.

    """
    rgb = hex_to_rgb(hex_color)
    ansi_escape = f"\033[38;2;{rgb[0]};{rgb[1]};{rgb[2]}m"
    reset_escape = "\033[0m"
    if auto_print:
        print(f"{ansi_escape}{string}{reset_escape}")
        return None
    return f"{ansi_escape}{string}{reset_escape}"


def check_env_variables():
    """

    Check this script global variables.

    Check this script global variables, defining the variable if it is present in environment
    variables and not defined in the script (This script initial global variables has higher
    preference, except for ZOTERO_TO_SIOYEK_COLORS). Print a warning message and exit if
    a needed variable is not defined neither in the script or environment variables.

    Parameters
    ----------
    None

    """
    exit_bool = False
    if os.getenv("ZOTERO_TO_SIOYEK_COLORS") is not None:
        globals()["ZOTERO_TO_SIOYEK_COLORS"] = ast.literal_eval(
            os.getenv("ZOTERO_TO_SIOYEK_COLORS"),
        )
    for k, v in {
        "ZOTERO_LIBRARY_ID": ZOTERO_LIBRARY_ID,
        "ZOTERO_LOCAL_DIR": ZOTERO_LOCAL_DIR,
        "ZOTERO_API_KEY": ZOTERO_API_KEY,
        "SIOYEK_LOCAL_DATABASE_FILE_PATH": SIOYEK_LOCAL_DATABASE_FILE_PATH,
        "SIOYEK_SHARED_DATABASE_FILE_PATH": SIOYEK_SHARED_DATABASE_FILE_PATH,
        "SIOYEK_PATH": SIOYEK_PATH,
    }.items():
        if v == "":
            value = os.getenv(k)
            if value is not None:
                globals()[k] = value
            else:
                print(f"{RED} {k}{RST} script variable needs to be defined")
                exit_bool = True

    if exit_bool:
        sys.exit()


def validate_arg(arg, type_str):
    """

    Validate a given argparse argument, based on the passed type.

    Parameters
    ----------
    arg : argparse.Namespace
        Argparse argument value.

    type_str : str
        String with the type that should be checked the arg, with the options:
            "float", "str", "tag", "int", "filename_in_lib"

    Returns
    -------
    bool

    Examples
    --------
    >>> print(validate_arg("24.4", "float"))
    True

    """
    if arg is None:
        return False

    if type_str in ("str", "tag"):
        try:
            isinstance(arg, str)
            return True
        except ValueError:
            print("Value must be a string!")
            return False

    if type_str == "int":
        try:
            isinstance(arg, int)
            return True
        except ValueError:
            print("Value must be an Integer!")
            return False

    if type_str == "existing_file":
        try:
            isinstance(arg, str)
            os.path.isfile(arg)
            return True
        except ValueError:
            print("Value must be and existing file Path!")

    if type_str == "tuple_to_datetime":
        if isinstance(arg, str):
            arg = tuple(arg)
        try:
            arg = datetime.datetime(arg)
            isinstance(arg, datetime.datetime)
            return arg
        except ValueError:
            print("\nValue must be a tuple of datetime!\n")
            return False

    if type_str == "sort":
        try:
            assert arg in (
                "dateAdded",
                "dateModified",
                "title",
                "creator",
                "type",
                "date",
                "publisher",
                "publicationTitle",
                "journalAbbreviation",
                "language",
                "accessDate",
                "libraryCatalog",
                "callNumber",
                "rights",
                "addedBy",
                "numItems",
                "tags",
            )
            return True
        except ValueError:
            print("\nValue must be a pyzotero valid sort string!\n")
            return False

    else:
        return True


def check_args_number(argnsp, argument_name, type_list, parser, zotero_data=None):
    """

    Cheks argparse passed number of arguments.

    Checks numbers of arguments passed to an specific argparse flag, and
     if this number is lower than the length of the argument metravar,
     a prompt is activated to the user to input the missing arguments.
    Also checks if arguments type are correct, as well as argument
    range. If any of the checkings fail, the user is inputted to
    reinsert the argument.

    Parameters
    ----------
    argnsp : list
        argparse argument

    argument_name : str
        str of the name from the argparse argument.
        args.argument_name=argnsp

    type_list : list
        list of strings, containing the argument values types, to be passed
        to the validate_arg function

    Returns
    -------
    none

    """
    if argnsp is None:
        argnsp = []

    currentlen = len(argnsp)

    for action in parser._actions:
        if argument_name in action.option_strings:
            lenargs = len(action.metavar)
            if currentlen != lenargs:
                while currentlen < lenargs:
                    input_text = "Insert Argument: "
                    curr_options = " ".join(reversed(action.option_strings))
                    curr_metas = " ".join(action.metavar)
                    print(f"\n{curr_options} [{curr_metas}]\n")
                    input_text = f"{action.metavar[currentlen]}: "
                    if type_list[currentlen] == "tag" and zotero_data is not None:
                        tags_str = zotero_data.get_zotero_tags_by_pdf_path(argnsp[currentlen - 1])
                        print(f"{CYAN}Tags\n----{RST}\n{tags_str}\n")
                        input_text = "Tag: "
                    new_arg = input(input_text)
                    if (new_arg.startswith('"') and new_arg.endswith('"')) or (
                        new_arg.startswith("'") and new_arg.endswith("'")
                    ):
                        new_arg = new_arg[1:-1]
                    check_validate = validate_arg(new_arg, type_list[currentlen])
                    if isinstance(check_validate, str):
                        argnsp.append(check_validate)
                    else:
                        argnsp.append(new_arg)
                    currentlen = len(argnsp)
                    print("\n")
            else:
                for n in range(0, lenargs - 1):
                    exc_validate = validate_arg(argnsp[n], type_list[n])
                    while not exc_validate:
                        new_arg = input("Insert Argument: ")
                        argnsp[n] = new_arg


def print_gen_help(parser):
    """

    Print this script sclient help message.

    Parameters
    ----------
    parser : argparse.ArgumentParser
        argparse parser class object.

    Returns
    -------
    None

    """
    group_colors = [f"{GREEN}", f"{RED}", f"{CYAN}", f"{MGN}", f"{BLUE}"]
    line_list = []
    group_desc_list = []
    line_str_group = []
    headers_sep = " " * (30)
    for group in parser._action_groups:
        if group.title and group.description is not None:
            for action in group._group_actions:
                tmp_list = []
                flag = ", ".join(reversed(action.option_strings))
                if action.metavar is not None:
                    for n in action.metavar:
                        tmp_list.append(f"[{n}]")
                    metas = ", ".join(tmp_list)
                else:
                    metas = ""
                hnew = " " * (35 - len(flag))
                line_list.append(f"{BLUE}{flag}{RST}{hnew}{YELLOW}{metas}{RST}\n{action.help}")
            group_desc_list.append(f"{group.description}\n")
            line_str_group.append("\n".join(line_list))
            line_list = []

    print(
        f"\n{parser.prog}\n\n{parser.description}\n\n"
        f"{BLUE}FLAGS{RST}{headers_sep}{YELLOW}ARGUMENTS{RST}\n"
        f"{BLUE}====={RST}{headers_sep}{YELLOW}=========={RST}\n"
    )
    for idx, value in enumerate(line_str_group):
        print(
            f"\n{group_colors[idx]}{group_desc_list[idx]}{'-' * len(group_desc_list[idx])}\n{RST}"
        )
        print(f"{value}")
    print(f"\n{parser.epilog}")


def print_group_help(parser, group_title):
    """

    Print to terminal the help function from one of the available argparse groups.

    The group is passed as flag, and can be: sioyek; zotero; general.

    Parameters
    ----------
    parser : argparse.ArgumentParser
        argparse parser class object.

    group_title : str
        Name of the group to print the help

    """
    for group in parser._action_groups:
        if group.title == group_title and group.description is not None:
            print(f"\n{group.description}\n")
            for action in group._group_actions:
                action_join = " ".join(action.option_strings)
                meta_join = " ".join(action.metavar) if action.metavar is not None else ""
                print(f"{MGN}{action_join}{RST}  {YELLOW}{meta_join}{RST}\n{action.help}\n")


def cli_args_general_utils(args, parser):
    """

    Help handling function.

    Handle the -h/--help flags, to check for any passed arguments, in the case of specific
    argparse groups help printing.

    Parameters
    ----------
    parser : argparse.ArgumentParser
        argparse parser class object.

    group_title : str
        Name of the group to print the help

    """
    if args.help is None:
        args.help = []
    if len(args.help) == 0:
        if "-h" in sys.argv:
            parser.print_help()
        else:
            print_gen_help(parser)
        return

    for n in args.help:
        n = str(n)
        if n and n[0].islower():
            n = n[0].upper() + n[1:]
        print_group_help(parser, n)


def argparse_parser(opt_args: Optional[str] = None):
    """

    Parse argparse groups and arguments.

    Parameters
    ----------
    opt_args : list, optional
        Optional argparse list of arguments, used to pass arguments to the function without using
        a terminal, usefull for testing arguments in doctest for example (defaults to None)

    Returns
    -------
    args : argparse.Namespace

    parser : argparse.ArgumentParser

    Examples
    --------
    Displaying some argparse parser features

    >>> args, parser = argparse_parser(["--help"])

    >>> print(parser.prog)
    python zot2sioyek.py [FLAG] [ARGUMENTS]

    >>> print(parser.description)
    Zotero highlights to sioyek manager.
    If any necessary argument is not given, the user will be prompted to input it.

    Flags that where passed, that don't take arguments, behave like the following

    >>> print(args.help)
    []

    Flags options that exists but where not passed behave like the following

    >>> print(args.add_zotero_tag)
    None

    Getting the testing PDF path for some tests

    >>> test_pdf = os.path.abspath(os.getcwd()) + "/tests/E5M6X2IH/test.pdf"

    Flags that takes a pdf file path as argument, behave like the following with valid paths

    >>> args, parser = argparse_parser(["--get-highlights", test_pdf])
    >>> print(os.path.basename(args.get_highlights[0]))
    test.pdf

    Like the following given a zotero item title

    >>> args, parser = argparse_parser(["--get-highlights", "Zotero Item Title"])
    >>> print(args.get_highlights)
    ['Zotero Item Title']

    And like the following if is passed a string that is a invalid patter or title

    >>> args, parser = argparse_parser(["--get-highlights", "/invalid/path/doc.pdf"])

    """  # noqa: D301
    parser = argparse.ArgumentParser(
        prog="python zot2sioyek.py [FLAG] [ARGUMENTS]",
        description=textwrap.dedent(
            """\
            Zotero highlights to sioyek manager.
            If any necessary argument is not given, the user will be prompted to input it."""
        ),
        epilog=textwrap.dedent(
            """\
            If an argument passed after a flag contain blank spaces, remember to quote wrap it,
            while not being necessary case inputted after through prompted option.

            Author: eduardotcampos@usp.br\
        """
        ),
        allow_abbrev=True,
        add_help=False,
    )

    group_general = parser.add_argument_group(
        "General",
        description="Script general utils.",
    )

    group_zotero = parser.add_argument_group(
        "Zotero",
        description="Zotero Managing Commands.",
    )

    group_sioyek = parser.add_argument_group(
        "Sioyek",
        description="Sioyek Main Commands.",
    )

    group_extras = parser.add_argument_group(
        "Extras",
        description="Extra options flags.",
    )

    group_general.add_argument(
        "--help",
        "-h",
        help=textwrap.dedent(
            """\
             Print this script help.
             If a Group name is passed after --help, the help to this specific group is printted
             only. Available groups are: general, zotero, sioyek.\
         """
        ),
        nargs="*",
    )

    group_zotero.add_argument(
        "--get-highlights",
        "-g",
        type=str,
        nargs="*",
        action="store",
        help="Print all highlights from a given zotero file.",
        metavar=("file_name_or_path",),
    )
    group_zotero.add_argument(
        "--print-annotation-text",
        "-p",
        type=str,
        nargs="*",
        action="store",
        help="print all highlighted text for a given zotero PDF local file.",
        metavar=("file_name_or_path",),
    )

    group_zotero.add_argument(
        "--zotero-tags",
        "-T",
        nargs="*",
        metavar=("file_name_or_path",),
        action="store",
        help="Prints a zotero PDF attachment parent item existing arguments.",
    )

    group_zotero.add_argument(
        "--add-zotero-tag",
        "-A",
        nargs="*",
        metavar=(
            "file_name_or_path",
            "tag_str_to_add",
        ),
        action="store",
        help=textwrap.dedent(
            """\
             Add a tag to a zotero PDF attachment parent item. Takes arguments file name or
             path, and tag str to add.\
         """
        ),
    )

    group_zotero.add_argument(
        "--remove-zotero-tag",
        "-R",
        nargs="*",
        metavar=(
            "file_name_or_path",
            "tag_str_to_remove",
        ),
        action="store",
        help=textwrap.dedent(
            """\
             Remove a tag from a zotero PDF attachment parent item. Takes arguments file name or
             path, and tag str to remove.\
         """
        ),
    )

    group_sioyek.add_argument(
        "--list-sioyek-files",
        "-f",
        action="store_true",
        help="Print all files in sioyek local database",
    )

    group_sioyek.add_argument(
        "--list-sioyek-hash",
        "-H",
        type=str,
        nargs="*",
        action="store",
        help="print a sioyek database pdf file md5sum hash.",
        metavar=("file_name_or_path",),
    )

    group_sioyek.add_argument(
        "--print-sioyek-attributes",
        "-l",
        type=str,
        nargs="*",
        metavar=("file_name_or_path",),
        action="store",
        help="Print all Attributes and values in a sioyek database PDF file.",
    )

    group_sioyek.add_argument(
        "--insert-highlight",
        "-i",
        nargs="*",
        metavar=("file_name_or_path",),
        action="store",
        help=textwrap.dedent(
            """\
             Insert highlights in a sioyek database PDF file, importing this highlights from this
             PDF file zotero attachment highlight.\
         """
        ),
        type=str,
    )

    group_sioyek.add_argument(
        "--insert-dated-highlight",
        "-d",
        nargs="*",
        action="store",
        metavar=("datetime.datetime",),
        type=str,
        help=textwrap.dedent(
            """\
             Insert highlights in multiple sioyek database PDF files, importing this highlights from this
             based on the passed arguments of a datetime.datetime date, to start from to search
             for highlights, limit_number_items, that sets the maximum of items to retrieve, and
             sort method that organize the order of the retrieved items.\
         """
        ),
    )

    group_sioyek.add_argument(
        "--list-all-sioyek-highlights",
        "-S",
        action="store_true",
        help="Print all sioyek highlights",
    )

    group_sioyek.add_argument(
        "--newdu",
        action="store_true",
        help="Test",
    )

    group_sioyek.add_argument(
        "--citation-key",
        "-k",
        help="Print zotero PDF file parent citation key.",
        action="store",
        nargs="*",
        type=str,
        metavar=("file_name_or_path",),
    )

    group_sioyek.add_argument(
        "--undo-last",
        "-u",
        help="Undo last highlighting bath operation.",
        action="store_true",
    )

    group_sioyek.add_argument(
        "--delete-highlights",
        "-D",
        help="Delete all highlights from a sioyek file.",
        action="store",
        nargs="*",
        type=str,
        metavar=("file_name_or_path",),
    )

    group_extras.add_argument(
        "--shared-database",
        nargs="*",
        action="store",
        metavar=("path_db_file",),
        type=str,
        help="Path to a different shared database then defined in env variables or in the script.",
    )

    group_extras.add_argument(
        "--local-database",
        nargs="*",
        action="store",
        metavar=("path_db_file",),
        type=str,
        help="Path to a different local database then defined in env variables or in the script.",
    )

    group_extras.add_argument(
        "--method",
        nargs="*",
        action="store",
        metavar=("Highlighting_Method",),
        type=str,
        choices=[
            "fitz",
            "custom",
            "zotero",
        ],
        help="Method used to identify and transfere the highlights from zotero to sioyek.",
    )

    (
        group_extras.add_argument(
            "--sort",
            nargs="*",
            action="store",
            metavar=("pyzotero_sort_strategy",),
            choices=[
                "dateAdded",
                "dateModified",
                "title",
                "creator",
                "type",
                "date",
                "publisher",
                "publicationTitle",
                "journalAbbreviation",
                "language",
                "accessDate",
                "libraryCatalog",
                "callNumber",
                "rights",
                "addedBy",
                "numItems",
                "tags",
            ],
            type=str,
            help="Pyzotero items sorting method. Requires to have passed --insert-dated-highlight.",
        ),
    )
    if opt_args is not None:
        args = parser.parse_args(opt_args)
    else:
        args = parser.parse_args()

    return args, parser


def cli(opt_args=None):
    """

    Read main argparse client function, read the user passed flags, and exec functions based on it.

    Parameters
    ----------
    None
    """
    check_env_variables()
    args, parser = argparse_parser(opt_args)

    if len(sys.argv) <= 1:
        cli_args_general_utils(args, parser)
        return

    if args.help is not None:
        cli_args_general_utils(args, parser)

    if args.shared_database is not None:
        globals()["SIOYEK_SHARED_DATABASE_FILE_PATH"] = args.shared_database[0]

    if args.local_database is not None:
        globals()["SIOYEK_LOCAL_DATABASE_FILE_PATH"] = args.local_database[0]

    zotero_data = ZoteroData(
        library_id=ZOTERO_LIBRARY_ID,
        library_type=ZOTERO_LIBRARY_TYPE,
        api_key=ZOTERO_API_KEY,
    )

    sioyek_data = SioyekData(
        local_database_file_path=SIOYEK_LOCAL_DATABASE_FILE_PATH,
        shared_database_file_path=SIOYEK_SHARED_DATABASE_FILE_PATH,
        sioyek_path=SIOYEK_PATH,
    )

    if args.get_highlights is not None:
        check_args_number(
            args.get_highlights,
            "--get-highlights",
            ["filename_in_lib"],
            parser,
        )
        file_path = args.get_highlights[0]
        zotero_data.print_get_highlights(file_path, sioyek_data)

    if args.print_annotation_text is not None:
        check_args_number(
            args.print_annotation_text,
            "--print-annotation-text",
            ["filename_in_lib"],
            parser,
        )

        file_path = args.print_annotation_text[0]
        zotero_data.extract_highlights(clean_path(file_path))
        for n in zotero_data.highlights:
            print_colored_string(n.text, n.color)

    if args.list_sioyek_files:
        sioyek_data.list_files()

    if args.list_sioyek_hash is not None:
        check_args_number(
            args.list_sioyek_hash,
            "--list-sioyek-hash",
            ["filename_in_lib"],
            parser,
        )
        file_path = args.list_sioyek_hash[0]
        sioyek_data.list_hash(file_path)

    if args.print_sioyek_attributes is not None:
        check_args_number(
            args.print_sioyek_attributes,
            "--print-sioyek-attributes",
            ["filename_in_lib"],
            parser,
        )
        file_path = args.print_sioyek_attributes[0]
        print(file_path)
        if not os.path.isfile(file_path):
            file_path = zotero_data.get_local_pdf_path_by_title(file_path)
        sioyek_data.print_attributes(clean_path(file_path))

    if args.insert_highlight is not None:
        check_args_number(
            args.insert_highlight,
            "--insert-highlight",
            ["filename_in_lib"],
            parser,
        )
        file_path = args.insert_highlight[0]
        if args.method is not None:
            curr_method = args.method[0]
            sioyek_data.insert_highlight(clean_path(file_path), zotero_data, method=curr_method)
        else:
            sioyek_data.insert_highlight(clean_path(file_path), zotero_data)

    if args.insert_dated_highlight is not None:
        check_args_number(
            args.insert_dated_highlight,
            "--insert-dated-highlight",
            ["tuple_to_datetime"],
            parser,
        )
        check_args_number(
            args.sort,
            "--sort",
            ["optional sort"],
            parser,
        )
        date = args.insert_dated_highlight[0]
        zotero_data.get_highlights_by_date(date)

    if args.list_all_sioyek_highlights:
        sioyek_data.list_all_sioyek_highlights()

    if args.zotero_tags is not None:
        check_args_number(
            args.zotero_tags,
            "--zotero-tags",
            ["filename_in_lib"],
            parser,
        )
        file_path = args.zotero_tags[0]
        tags_str = zotero_data.get_zotero_tags_by_pdf_path(clean_path(file_path))
        tags_sioyek = " ".join(tags_str.split(","))
        if sioyek_data.sioyek.connected:
            subprocess.run([
                clean_path(SIOYEK_PATH),
                "--execute-command",
                "set_status_string",
                "--execute-command-data",
                tags_sioyek,
            ])
        print(tags_str)

    if args.add_zotero_tag is not None:
        check_args_number(
            args.add_zotero_tag,
            "--add-zotero-tag",
            ["filename_in_lib", "tag"],
            parser,
            zotero_data,
        )
        file_path = args.add_zotero_tag[0]
        added_tag = args.add_zotero_tag[1]
        zotero_data.add_zotero_tag_by_pdf_path(clean_path(file_path), added_tag)

    if args.remove_zotero_tag is not None:
        check_args_number(
            args.remove_zotero_tag,
            "--remove-zotero-tag",
            ["filename_in_lib", "tag"],
            parser,
            zotero_data,
        )
        file_path = args.remove_zotero_tag[0]
        removed_tag = args.remove_zotero_tag[1]
        zotero_data.remove_zotero_tag_by_pdf_path(clean_path(file_path), removed_tag)

    if args.undo_last:
        sioyek_data.undo_last()

    if args.delete_highlights is not None:
        check_args_number(
            args.delete_highlights,
            "--delete-highlights",
            ["filename_in_lib"],
            parser,
        )
        file_path = args.delete_highlights[0]
        sioyek_data.delete_highlights(file_path)

    if args.citation_key is not None:
        check_args_number(
            args.citation_key,
            "--citation-key",
            ["filename_in_lib"],
            parser,
            zotero_data,
        )
        file_path = args.citation_key[0]
        extra_key = zotero_data.get_pdf_cite_key(clean_path(file_path))
        if sioyek_data.sioyek.connected and extra_key is not None:
            subprocess.run([
                clean_path(SIOYEK_PATH),
                "--execute-command",
                "set_status_string",
                "--execute-command-data",
                extra_key,
            ])
        if extra_key is None or extra_key == "":
            print(f"{RED}Citation key not found!{RST}")
        elif isinstance(extra_key, list):
            for n in extra_key:
                print(n)
        else:
            print(extra_key)

    if args.newdu:
        print("TESTE")

    for n in [
        sioyek_data.local_db,
        sioyek_data.shared_db,
        sioyek_data.doc,
    ]:
        if n is not None:
            n.close()


if __name__ == "__main__":
    cli()
