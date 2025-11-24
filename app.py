import os
import numpy as np
import streamlit as st
import nltk
import language_tool_python
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sentence_transformers import SentenceTransformer, util

st.set_page_config(layout="wide", page_title="Nirmaan AI Task")

@st.cache_resource
def get_models():
    for r in ['punkt', 'vader_lexicon', 'punkt_tab']:
        try:
            nltk.data.find(f'tokenizers/{r}')
        except LookupError:
            nltk.download(r, quiet=True)

    bert = SentenceTransformer('all-MiniLM-L6-v2')
    tool = language_tool_python.LanguageTool('en-US')
    vader = SentimentIntensityAnalyzer()
    
    return bert, tool, vader

embedder, lang_tool, sentiment = get_models()

class Grader:
    def __init__(self, text, duration=60):
        self.raw_text = text
        self.sents = sent_tokenize(text)
        self.words = word_tokenize(text)
        self.n_words = len(self.words)
        self.duration = duration
        self.wpm = (self.n_words / duration) * 60 if duration else 0

    def content_score(self):
        score = 0
        logs = []
        feedback = []
        
        # Salutation check
        lower = self.raw_text.lower()
        greetings = ["hello", "good morning", "good afternoon", "hi everyone", "myself", "hey"]
        if any(x in lower for x in greetings):
            score += 5
            feedback.append("Salutation present")
        else:
            feedback.append("No salutation found")

        # Topics check
        required = {
            "Identity": ["name", "myself", "i am"],
            "Age": ["years old", "age"],
            "Education": ["school", "class", "study", "college"],
            "Family": ["family", "mother", "father", "parents"],
            "Hobbies": ["hobby", "play", "cricket", "reading", "enjoy"],
            "Ambition": ["goal", "ambition", "dream", "become", "science", "engineer"],
            "Unique": ["fact", "unique", "special", "secret"]
        }
        
        hits = 0
        doc_emb = embedder.encode(self.sents, convert_to_tensor=True)

        for topic, keys in required.items():
            # Keyword match
            if any(k in lower for k in keys):
                hits += 1
                logs.append(f"{topic}: Keyword match")
                continue
            
            # Semantic match
            query = embedder.encode(f"My {topic} is", convert_to_tensor=True)
            sim = util.cos_sim(query, doc_emb)[0]
            
            if max(sim) > 0.4:
                hits += 1
                logs.append(f"{topic}: Semantic match")
        
        pts = min(30, int(hits * 4.3))
        score += pts
        feedback.append(f"Content coverage: {hits}/7 topics")

        # Structure flow
        if len(self.sents) > 2:
            score += 5
            feedback.append("Flow is logical")
        
        return score, feedback, logs

    def speed_score(self):
        w = self.wpm
        if 111 <= w <= 140:
            return 10, [f"Pace is ideal: {int(w)} WPM"]
        elif 81 <= w <= 160:
            return 6, [f"Pace acceptable: {int(w)} WPM"]
        return 2, [f"Pace issue: {int(w)} WPM"]

    def grammar_score(self):
        errs = len(lang_tool.check(self.raw_text))
        rate = (errs / self.n_words) * 100 if self.n_words else 0
        
        # 1 - min(errors_per_100 / 10, 1)
        metric = 1 - min(rate / 10, 1)
        
        g_pts = 4
        if metric > 0.9: g_pts = 10
        elif metric > 0.7: g_pts = 8

        # TTR
        uniq = len(set(w.lower() for w in self.words))
        ttr = uniq / self.n_words if self.n_words else 0
        
        v_pts = 6
        if ttr > 0.5: v_pts = 10
        elif ttr > 0.4: v_pts = 8
        
        return g_pts + v_pts, [f"Grammar errors: {errs}", f"Vocab score: {v_pts}/10"]

    def clarity_score(self):
        bad_words = ['um', 'uh', 'like', 'you know', 'actually', 'basically']
        cnt = sum(1 for w in self.words if w.lower() in bad_words)
        ratio = (cnt / self.n_words) * 100 if self.n_words else 0
        
        pts = 6
        if ratio <= 3: pts = 15
        elif ratio <= 6: pts = 12
        
        return pts, [f"Fillers: {cnt} ({int(ratio)}%)"]

    def sentiment_score(self):
        p = sentiment.polarity_scores(self.raw_text)['pos']
        if p > 0.15: return 15, ["Tone: High engagement"]
        if p > 0.1: return 12, ["Tone: Moderate"]
        return 9, ["Tone: Neutral"]

    def run(self):
        c, c_fb, logs = self.content_score()
        s, s_fb = self.speed_score()
        g, g_fb = self.grammar_score()
        cl, cl_fb = self.clarity_score()
        e, e_fb = self.sentiment_score()
        
        return {
            "total": c + s + g + cl + e,
            "details": {
                "Content (40%)": {"val": c, "msg": c_fb, "logs": logs},
                "Speed (10%)": {"val": s, "msg": s_fb},
                "Grammar (20%)": {"val": g, "msg": g_fb},
                "Clarity (15%)": {"val": cl, "msg": cl_fb},
                "Engagement (15%)": {"val": e, "msg": e_fb}
            }
        }

# UI
st.title("Evaluation Tool")

with st.sidebar:
    sec = st.slider("Duration (sec)", 30, 300, 52)

try:
    with open("data/sample_text.txt", "r") as f:
        default_val = f.read()
except:
    default_val = ""

txt = st.text_area("Input Transcript", value=default_val, height=200)

if st.button("Calculate"):
    if not txt.strip():
        st.error("No text provided")
    else:
        g = Grader(txt, sec)
        res = g.run()
        
        st.metric("Final Score", f"{res['total']}/100")
        
        for k, v in res['details'].items():
            with st.expander(f"{k}: {v['val']}"):
                for m in v['msg']:
                    st.write(f"- {m}")
                if 'logs' in v and v['logs']:
                    st.caption("Debug info:")
                    st.write(v['logs'])
        
        st.json(res)