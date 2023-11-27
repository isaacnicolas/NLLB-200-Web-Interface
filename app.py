import streamlit as st
import sentencepiece as spm
import ctranslate2

# Set default parameters
source_lang = ""
target_lang = ""

available_models = ["nllb-200-distilled-600M"]


langs = ["Select a language...","ace_Arab",  "bam_Latn",  "dzo_Tibt",  "hin_Deva",	"khm_Khmr",  "mag_Deva",  "pap_Latn",  "sot_Latn",	"tur_Latn",
"ace_Latn",  "ban_Latn",  "ell_Grek",  "hne_Deva",	"kik_Latn",  "mai_Deva",  "pbt_Arab",  "spa_Latn",	"twi_Latn",
"acm_Arab",  "bel_Cyrl",  "eng_Latn",  "hrv_Latn",	"kin_Latn",  "mal_Mlym",  "pes_Arab",  "srd_Latn",	"tzm_Tfng",
"acq_Arab",  "bem_Latn",  "epo_Latn",  "hun_Latn",	"kir_Cyrl",  "mar_Deva",  "plt_Latn",  "srp_Cyrl",	"uig_Arab",
"aeb_Arab",  "ben_Beng",  "est_Latn",  "hye_Armn",	"kmb_Latn",  "min_Arab",  "pol_Latn",  "ssw_Latn",	"ukr_Cyrl",
"afr_Latn",  "bho_Deva",  "eus_Latn",  "ibo_Latn",	"kmr_Latn",  "min_Latn",  "por_Latn",  "sun_Latn",	"umb_Latn",
"ajp_Arab",  "bjn_Arab",  "ewe_Latn",  "ilo_Latn",	"knc_Arab",  "mkd_Cyrl",  "prs_Arab",  "swe_Latn",	"urd_Arab",
"aka_Latn",  "bjn_Latn",  "fao_Latn",  "ind_Latn",	"knc_Latn",  "mlt_Latn",  "quy_Latn",  "swh_Latn",	"uzn_Latn",
"als_Latn",  "bod_Tibt",  "fij_Latn",  "isl_Latn",	"kon_Latn",  "mni_Beng",  "ron_Latn",  "szl_Latn",	"vec_Latn",
"amh_Ethi",  "bos_Latn",  "fin_Latn",  "ita_Latn",	"kor_Hang",  "mos_Latn",  "run_Latn",  "tam_Taml",	"vie_Latn",
"apc_Arab",  "bug_Latn",  "fon_Latn",  "jav_Latn",	"lao_Laoo",  "mri_Latn",  "rus_Cyrl",  "taq_Latn",	"war_Latn",
"arb_Arab",  "bul_Cyrl",  "fra_Latn",  "jpn_Jpan",	"lij_Latn",  "mya_Mymr",  "sag_Latn",  "taq_Tfng",	"wol_Latn",
"arb_Latn",  "cat_Latn",  "fur_Latn",  "kab_Latn",	"lim_Latn",  "nld_Latn",  "san_Deva",  "tat_Cyrl",	"xho_Latn",
"ars_Arab",  "ceb_Latn",  "fuv_Latn",  "kac_Latn",	"lin_Latn",  "nno_Latn",  "sat_Olck",  "tel_Telu",	"ydd_Hebr",
"ary_Arab",  "ces_Latn",  "gaz_Latn",  "kam_Latn",	"lit_Latn",  "nob_Latn",  "scn_Latn",  "tgk_Cyrl",	"yor_Latn",
"arz_Arab",  "cjk_Latn",  "gla_Latn",  "kan_Knda",	"lmo_Latn",  "npi_Deva",  "shn_Mymr",  "tgl_Latn",	"yue_Hant",
"asm_Beng",  "ckb_Arab",  "gle_Latn",  "kas_Arab",	"ltg_Latn",  "nso_Latn",  "sin_Sinh",  "tha_Thai",	"zho_Hans",
"ast_Latn",  "crh_Latn",  "glg_Latn",  "kas_Deva",	"ltz_Latn",  "nus_Latn",  "slk_Latn",  "tir_Ethi",	"zho_Hant",
"awa_Deva",  "cym_Latn",  "grn_Latn",  "kat_Geor",	"lua_Latn",  "nya_Latn",  "slv_Latn",  "tpi_Latn",	"zsm_Latn",
"ayr_Latn",  "dan_Latn",  "guj_Gujr",  "kaz_Cyrl",	"lug_Latn",  "oci_Latn",  "smo_Latn",  "tsn_Latn",	"zul_Latn",
"azb_Arab",  "deu_Latn",  "hat_Latn",  "kbp_Latn",	"luo_Latn",  "ory_Orya",  "sna_Latn",  "tso_Latn",
"azj_Latn",  "dik_Latn",  "hau_Latn",  "kea_Latn",	"lus_Latn",  "pag_Latn",  "snd_Arab",  "tuk_Latn",
"bak_Cyrl",  "dyu_Latn",  "heb_Hebr",  "khk_Cyrl",	"lvs_Latn",  "pan_Guru",  "som_Latn",  "tum_Latn"]

# Functions

def translate(source, translator, sp_model, source_lang, target_lang):
    """Use CTranslate model to translate a sentence

    Args:
        source (str): Source sentences to translate
        translator (object): Object of Translator, with the CTranslate2 model
        sp_source_model (object): Object of SentencePieceProcessor, with the SentencePiece source model
        sp_target_model (object): Object of SentencePieceProcessor, with the SentencePiece target model
    Returns:
        Translation of the source text
    """

    source_sents = [source]
    source_sentences = [sent.strip() for sent in source_sents]
    target_prefix = [[target_lang]] * len(source_sentences)

    # Subword the source sentences
    source_sents_subworded = sp_model.encode_as_pieces(source_sentences)
    source_sents_subworded = [[source_lang] + sent + ["</s>"] for sent in source_sents_subworded]
    
    # Translate the source sentences
    translations_subworded = translator.translate_batch(source_sents_subworded, batch_type="tokens", max_batch_size=2024, beam_size=4, target_prefix=target_prefix)
    translations_subworded = [translation.hypotheses[0] for translation in translations_subworded]
    for translation in translations_subworded:
        if target_lang in translation:
            translation.remove(target_lang)

    # Desubword the target sentences
    translations = sp_model.decode(translations_subworded)
    translation = translations[0]
  
    return translation

def load_model(option_model):
    """
    Loads the model according to the option_model selected

    Args:
        option_model(str): Model to use for the language direction

    Returns
        translator: ctranslate2.Translator object
        sp_source_model: spm.SentencepieceProcessor object for the source lang
        sp_target_model: spm.SentencepieceProcessor object for the target lang
    """

    if option_model == "nllb-200-distilled-600M":
        ct_model_path = "nllb-200_600M_int8_ct2/nllb-200-distilled-600M-int8/"
        sp_model_path = "flores200_sacrebleu_tokenizer_spm.model"
                
    # Create objects of CTranslate2 Translator and SentencePieceProcessor to load the models
    translator = ctranslate2.Translator(ct_model_path, "cpu")    # or "cuda" for GPU
    sp_model = spm.SentencePieceProcessor(sp_model_path)
    

    return translator, sp_model

# Title for the page and nice icon
st.set_page_config(page_title="Demo NLLB", layout="wide")

# Header
st.title("Demo NLLB Translate")

# Language Selection
left, right = st.columns(2)
with left: 
    source_lang = st.selectbox(
        "Select Source Language",
        langs,
        key='source_lang_selection',
        )
with right:
    target_lang = st.selectbox(
        "Select Target Language",
        langs,
        key='target_lang_selection'
        )

# Model Selection
option_model = st.selectbox(
    "Select a Model",
    available_models,
    key='model_selection'
    )

# Load model
translator, sp_model = load_model(option_model)

# Form to add your items
with st.form("my_form"):  
   
   # Textarea to type the source text.
    user_input = st.text_area("Source Text", max_chars=500)

    # Translate with CTranslate2 model
    translation = translate(user_input, translator, sp_model, source_lang, target_lang)

    # Create a button
    submitted = st.form_submit_button("Translate")
    # If the button is pressed, print the translation
    if submitted:
        st.write("Translation")
        st.info(translation)


# Optional Style
# Source: https://towardsdatascience.com/5-ways-to-customise-your-streamlit-ui-e914e458a17c
padding = 0
st.markdown(f""" <style>
    .reportview-container .main .block-container{{
        padding-top: {padding}rem;
        padding-right: {padding}rem;
        padding-left: {padding}rem;
        padding-bottom: {padding}rem;
    }} </style> """, unsafe_allow_html=True)


st.markdown(""" <style>
#MainMenu {visibility: visible;}
footer {visibility: hidden;}
</style> """, unsafe_allow_html=True)
