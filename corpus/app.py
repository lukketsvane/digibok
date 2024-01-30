import streamlit as st
import pandas as pd
import datetime
import dhlab as dh
import subprocess
import os
from io import BytesIO

max_size_corpus = 20000
max_rows = 1200
min_rows = 800
default_size = 10  

def to_excel(df):
    """Make an excel object out of a dataframe as an IO-object"""
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Sheet1")
    # worksheet = writer.sheets["Sheet1"]
    processed_data = output.getvalue()
    return processed_data


def v(x):
    "Turn empty string into None"
    if x != "":
        res = x
    else:
        res = None
    return res


def header():
    col_zero, col_two, col_three = st.columns([4, 1, 1])
    with col_zero:
        st.subheader("Definer et korpus med innholdsdata og metadata")
        link = "https://github.com/nationallibraryofnorway/dhlab-app-corpus"
        col_zero.markdown(
            f""" 
    <div style="display: flex; align-items: center; gap: 5px; margin-top: -20px;">


    
</div>
""",
            unsafe_allow_html=True,
        )

    with col_three:
        st.markdown(
            """<style>img {opacity: 0.6;}</style><a href="https://nb.no/dhlab"><img src="https://github.com/NationalLibraryOfNorway/DHLAB-apps/raw/main/corpus/DHlab_logo_web_en_black.png" style="width:250px"></a>""",
            unsafe_allow_html=True,
        )
    with st.expander("ℹ️ Appinfo"):
        # st.write("some text")
        st.markdown(
            """ 

vi tilbyr følgende ressurstyper:  
**Digibok**: Bøker fra Nasjonalbiblioteket  
**Digavis**: Aviser fra Nasjonalbiblioteket  
**Digitidsskrift**: Tidsskrift fra Nasjonalbiblioteket  
**Digistorting**: Stortingsdokumenter i NBs samling  
**Digimanus**: Brev og manuskripter  
**Kudos**: [Kunnskapsdokumenter i offentlig sektor](https://kudos.dfo.no/)  

"""
        )


def input_fields():
    def row1(params):
        col1, col2, col3 = st.columns([1, 1, 3])

        with col1:
            params["doctype"] = st.selectbox(
                "Type dokument",
                [
                    "digibok",
                    "digavis",
                    "digitidsskrift",
                    "digimanus",
                    "digistorting",
                    "kudos",
                ],
                help="Dokumenttypene følger Nasjonalbibliotekets digitale typer",
            )

        with col2:
            lang = st.multiselect(
                "Språk",
                [
                    "nob",
                    "nno",
                    "dan",
                    "swe",
                    "sme",
                    "smj",
                    "fkv",
                    "eng",
                    "fra",
                    "spa",
                    "ger",
                ],
                # default = "nob",
                help="Velg fra listen",
                disabled=(params["doctype"] in ["digistorting"]),
            )
            params["langs"] = " AND ".join(list(lang))

            if params["langs"] == "":
                params["langs"] = None

        with col3:
            today = datetime.date.today()
            year = today.year
            params["years"] = st.slider("Årsspenn", 1810, year, (1950, year))

    def row2(params):
        # st.subheader("Forfatter og tittel") ###################################################
        cola, colb = st.columns(2)

        with cola:
            params["authors"] = st.text_input(
                "Forfatter",
                "",
                help="Feltet blir kun tatt hensyn til for digibok",
                disabled=(params["doctype"] in ["digavis", "digistorting"]),
            )

        with colb:
            params["title"] = st.text_input(
                "Tittel",
                "",
                help="Søk etter titler. For aviser vil tittel matche avisnavnet.",
                disabled=(params["doctype"] in ["digistorting"]),
            )

    def row3(params):
        # st.subheader("Meta- og innholdsdata") ##########################################################

        cold, cole, colf = st.columns(3)
        with cold:
            params["fulltext"] = st.text_input(
                "Ord eller fraser i teksten",
                "",
                help="Matching på innholdsord skiller ikke mellom stor og liten bokstav."
                " Trunkert søk er mulig, slik at demokrat* vil finne bøker som inneholder demokrati og demokratisk blant andre treff",
            )

        with cole:
            params["ddk"] = st.text_input(
                "Dewey desimaltall",
                "",
                help="Input matcher et deweynummer. For å matche hele serien føy til en `*`. Bruk OR for å kombinere: 364* OR 916*",
                disabled=(params["doctype"] in ["digistorting"]),
            )

        with colf:
            params["subject"] = st.text_input(
                "Emneord",
                "",
                help="For å matche på flere emner, skill med OR for alternativ"
                " og AND for begrense. Trunkert søk går også — for eksempel vil barne* matche barnebok og barnebøker",
                disabled=(params["doctype"] in ["digistorting"]),
            )

    params = {}

    row1(params)
    row2(params)
    row3(params)

    return params


def corpus_management(params):
    df_defined = False
    st.subheader(
        "Lag korpuset og last ned metadata"
    )  ######################################################################

    with st.form(key="my_form"):
        colx, col_order, coly = st.columns([2, 2, 4])
        with colx:
            limit = st.number_input(
                f"Maks antall, inntil {max_size_corpus}",
                min_value=1,
                max_value=max_size_corpus,
                value=int(default_size * max_size_corpus / 100),
            )
            #    limit = st.number_input(300)
        with col_order:
            ordertype = st.selectbox(
                "Metode for uthenting",
                ["first", "rank", "random"],
                help="Metode 'first' er raskest, og velger dokument etter hvert som de blir funnet, mens'rank' gir en rask ordning på dokumenter om korpuset er definert med et fulltekstsøk og sorterer på relevans, siste valg er 'random' som først samler inn hele korpuset og gjør et vilkårlig utvalg av tekster derfra.",
            )
        with coly:
            filnavn = st.text_input("Filnavn for nedlasting", "korpus.xlsx")

        submit_button = st.form_submit_button(
            label="Trykk her når korpusdefinisjonen er klar"
        )

if submit_button:
    doctype = params["doctype"]
    if doctype == "digimanus":
        df = dh.Corpus(
            doctype=v(params["doctype"]),
            author=v(params["authors"]),
            fulltext=v(params["fulltext"]),
            from_year=params["years"][0],
            to_year=params["years"][1],
            title=v(params["title"]),
            limit=limit,
            order_by=ordertype,
        ).frame
        columns = ["dhlabid", "urn", "authors", "title", "timestamp", "year"]

    elif doctype == "digavis":
        df = dh.Corpus(
            doctype=v(params["doctype"]),
            fulltext=v(params["fulltext"]),
            from_year=params["years"][0],
            to_year=params["years"][1],
            title=v(params["title"]),
            limit=limit,
            order_by=ordertype,
        ).frame
        columns = ["urn", "title", "year", "timestamp", "city"]

    elif doctype == "digitidsskrift":
        df = dh.Corpus(
            doctype=v(params["doctype"]),
            author=v(params["authors"]),
            fulltext=v(params["fulltext"]),
            from_year=params["years"][0],
            to_year=params["years"][1],
            title=v(params["title"]),
            subject=v(params["subject"]),
            ddk=v(params["ddk"]),
            lang=params["langs"],
            limit=limit,
            order_by=ordertype,
        ).frame
        columns = [
            "dhlabid",
            "urn",
            "title",
            "city",
            "timestamp",
            "year",
            "publisher",
            "ddc",
            "langs",
        ]

    elif doctype == "digistorting":
        df = dh.Corpus(
            doctype=v(params["doctype"]),
            fulltext=v(params["fulltext"]),
            from_year=params["years"][0],
            to_year=params["years"][1],
            limit=limit,
            order_by=ordertype,
        ).frame
        columns = ["dhlabid", "urn", "year"]

    else:
        df = dh.Corpus(
            doctype=v(params["doctype"]),
            author=v(params["authors"]),
            fulltext=v(params["fulltext"]),
            from_year=params["years"][0],
            to_year=params["years"][1],
            title=v(params["title"]),
            subject=v(params["subject"]),
            ddk=v(params["ddk"]),
            lang=params["langs"],
            limit=limit,
            order_by=ordertype,
        ).frame
        columns = [
            "dhlabid",
            "urn",
            "authors",
            "title",
            "city",
            "timestamp",
            "year",
            "publisher",
            "ddc",
            "subjects",
            "langs",
        ]

    st.markdown(f"Fant totalt {len(df)} dokumenter")

    if len(df) >= max_rows:
        st.markdown(f"Viser {min_rows} rader.")
        st.dataframe(df[columns].sample(min(min_rows, max_rows)).astype(str))

    else:
        st.dataframe(df[columns].astype(str))

    df_defined = True

    if df_defined:
        if st.download_button(
            "Last ned data i excelformat",
            to_excel(df),
            filnavn,
            help="Åpnes i Excel eller tilsvarende",
        ):
            pass

    urn_value = st.text_input("Lim inn URN verdi her (feks., URN:NBN:no-nb_digibok_2020051148114)")

    if st.button('Download PDF'):
        if urn_value.startswith('URN:NBN:no-nb_'):
            identifier = urn_value.replace('URN:NBN:no-nb_', '')
            command = f"python3 nbno.py --id {identifier} --title --pdf"
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            output, error = process.communicate()
            
            st.text_area("Log output:", output.decode('utf-8'), height=150)
            
            if process.returncode == 0:
                # Find the most recently modified PDF file in the books directory
                books_dir = "books/"
                pdf_files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(books_dir) for f in filenames if f.endswith('.pdf')]
                latest_pdf_file = max(pdf_files, key=os.path.getmtime)
                
                if latest_pdf_file:
                    with open(latest_pdf_file, "rb") as pdf_file:
                        st.download_button(
                            label="Download PDF",
                            data=pdf_file,
                            file_name=os.path.basename(latest_pdf_file),
                            mime="application/pdf"
                        )
                else:
                    st.error("PDF file not found. Please check the nbno.py script's output directory.")
            else:
                st.error("An error occurred while downloading the PDF.")
                if error:
                    st.text_area("Error log:", error.decode('utf-8'), height=150)
        else:
            st.warning("Please enter a valid URN value.")



def main():
    ## Page configuration
    st.set_page_config(
        page_title="Korpus",
        page_icon=None,
        layout="wide",
        initial_sidebar_state="auto",
        menu_items=None,
    )
    st.markdown(
        '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">',
        unsafe_allow_html=True,
    )

    header()

    st.write("---")

    params = input_fields()

    corpus_management(params)


if __name__ == "__main__":
    main()
