#!/usr/bin/python

from .helpers.ankiflash import AnkiHelper

# The import mode is one of:
# UPDATE_MODE: update if first field matches existing note
# IGNORE_MODE: ignore if first field matches existing note
# ADD_MODE: import even if first field matches existing note
UPDATE_MODE = 0
IGNORE_MODE = 1
ADD_MODE = 2


class Importer:
    @staticmethod
    def is_note_type_diff(noteTypeName, front, back, css, mw):
        # Get note type
        noteType = mw.col.models.byName(noteTypeName)
        if noteType == None:
            return None

        # Get template
        tempates = noteType["tmpls"]
        for temp in tempates:
            if temp["name"] == "AnkiFlash":
                template = temp

        # Compare question
        asIsFrontMd5 = AnkiHelper.md5_utf8(template["qfmt"])
        toBeFrontMd5 = AnkiHelper.md5_utf8(front)
        if asIsFrontMd5 != toBeFrontMd5:
            return True

        # Compare answers
        asIsBackMd5 = AnkiHelper.md5_utf8(template["afmt"])
        toBeBackMd5 = AnkiHelper.md5_utf8(back)
        if asIsBackMd5 != toBeBackMd5:
            return True

        # Compate css
        asIsCssMd5 = AnkiHelper.md5_utf8(noteType["css"])
        toBeCssMd5 = AnkiHelper.md5_utf8(css)
        if asIsCssMd5 != toBeCssMd5:
            return True

        return False

    @staticmethod
    def create_note_type(noteTypeName, front, back, css, mw, mm):
        # Create empty note type
        nt = mm.new(noteTypeName)

        # Add fields into note type
        mm.add_field(nt, mm.new_field("Word"))
        mm.add_field(nt, mm.new_field("WordType"))
        mm.add_field(nt, mm.new_field("Phonetic"))
        mm.add_field(nt, mm.new_field("Example"))
        mm.add_field(nt, mm.new_field("Sound"))
        mm.add_field(nt, mm.new_field("Image"))
        mm.add_field(nt, mm.new_field("Meaning"))
        mm.add_field(nt, mm.new_field("Copyright"))

        # Add template into note type
        template = mm.new_template("AnkiFlash")
        template["qfmt"] = front
        template["afmt"] = back
        nt["css"] = css
        mm.add_template(nt, template)

        # Save model / note type
        mm.save(nt)

        # Update UI
        mw.reset()

    @staticmethod
    def update_note_type(noteTypeName, front, back, css, mw, mm):

        noteType = mw.col.models.byName(noteTypeName)
        if noteType == None:
            raise RuntimeError("{} Note type not found!".format(noteTypeName))

        # Get template
        tempates = noteType["tmpls"]
        for temp in tempates:
            if temp["name"] == "AnkiFlash":
                template = temp

        # Add template into note type
        template["qfmt"] = front
        template["afmt"] = back
        noteType["css"] = css

        # Save model / note type
        mm.save(noteType)

        # Update UI
        mw.reset()

    @staticmethod
    def import_text_file(deckName, mode, noteTypeName, mw, ti):
        # Select deck
        did = mw.col.decks.id(deckName)
        mw.col.decks.select(did)

        # Set note type for deck
        m = mw.col.models.by_name(noteTypeName)
        deck = mw.col.decks.get(did)
        deck["mid"] = m["id"]
        mw.col.decks.save(deck)

        # Import into the collection
        ti.model["id"] = m["id"]

        mw.col.set_aux_notetype_config(ti.model["id"], "lastDeck", did)
        mw.col.models.save(ti.model, updateReqs=False)

        if "1." in mode:
            ti.importMode = ADD_MODE
        elif "2." in mode:
            ti.importMode = UPDATE_MODE
        else:
            ti.importMode = IGNORE_MODE

        ti.delimiter = "\t"
        ti.allowHTML = True
        ti.open()
        ti.updateDelimiter()
        ti.run()

        # Update UI
        mw.reset()
