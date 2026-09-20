# Real files and document manifests

The optional Python helpers export actual single-column A4 PDF/DOCX documents,
extract source text, combine selected PDFs, and stage uploads. They make no
external network requests. Plain writing needs no Python dependencies.

Resolve `scripts/cvtool.py` against the toolkit root (or the installed skill
directory). Use an approved virtual environment with `scripts/requirements.txt`.
The examples below run from that root; substitute quoted absolute paths when
working elsewhere. Candidate output must be outside the skill checkout.

## Inspect and export

```sh
python scripts/cvtool.py inspect --file "../career/old-cv.docx"
python scripts/cvtool.py validate --kind profile --file "../career/profile.json"
python scripts/cvtool.py export --input "../career/cv-content.json" --format both --output "../career/applications/example-42/cv-v1"
```

`examples/document.json` is synthetic and demonstrates
`schemas/document.schema.json`. The agent writes final, evidence-backed content
to this structure before exporting. Output is a real `.docx` and/or `.pdf`.
Existing outputs are not overwritten; choose a versioned name. Known draft
placeholders fail export. Unicode uses an embedded PDF font; unsupported glyphs
produce a clear error so a suitable TTF can be supplied with `--font`.

Check the actual exported page count and extracted text. This catches missing
text and ordering problems; it does not prove an employer's ATS result. The
inspector reads TXT/MD/JSON, DOCX, and text PDFs. Image-only PDFs, photographs,
and unsupported formats need OCR/extraction elsewhere or supplied text.

## Stage selected files

```sh
python scripts/cvtool.py stage --workspace "../career/applications/example-42" --file "../career/applications/example-42/cv-v1.pdf" --id cv --kind cv --language en
python scripts/cvtool.py stage --workspace "../career/applications/example-42" --file "../career/cover-letter.pdf" --id letter --kind cover-letter --language en
```

The helper creates versioned files under `documents/` and a `documents.json`
manifest containing role, relative path, SHA-256, byte size, and language. CVs
and letters must be text-based PDF/DOCX with no known draft placeholders.
Supporting evidence may include scanned PDFs or PNG/JPEG originals.

Replacing the selected version of an existing ID requires `--replace`. Previous
files are retained. A previously recorded portal upload then fails review until
the new version is uploaded and verified. Do not edit staged files in place.

## Combined attachments

```sh
python scripts/cvtool.py merge --inputs "../career/cover-letter.pdf" "../career/certificate.pdf" --output "../career/other-documents-v1.pdf"
python scripts/cvtool.py stage --workspace "../career/applications/example-42" --file "../career/other-documents-v1.pdf" --id other --kind supporting --language en
```

Merge in the user's chosen order only when a portal needs one combined file.
Check it against the portal's actual size/type/count restrictions. Preserve
originals. Select `cv` and `other` for this application rather than also uploading
the component letter/certificate a second time. Encrypted PDFs require an
unlocked user-supplied copy. A renamed Markdown file is not a PDF.

## Upload to the browser

Use the manifest's selected files, resolved to absolute local paths accessible
to the MCP server. Verify hashes before upload. Native `browser_file_upload`
handles a chooser; equivalent browser tools may use a file input or drop target.
Check the portal's completed upload list and filenames afterwards, then record
an upload event. Successful local selection is not proof of a completed upload.
Never run a third-party online CV checker or transfer documents to a remote
browser without the user's explicit choice.
