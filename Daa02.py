import streamlit as st 
import random
import pandas as pd


# ---------------- Naive Search ----------------

def naive_search(text, pattern):
    n, m = len(text), len(pattern)
    matches = []
    comparisons = 0

    for i in range(n - m + 1):
        j = 0

        while j < m:
            comparisons += 1

            if text[i + j] != pattern[j]:
                break

            j += 1

        if j == m:
            matches.append(i)

    return matches, comparisons


# ---------------- KMP Algorithm ----------------

def compute_lps(pattern):
    m = len(pattern)
    lps = [0] * m

    length = 0
    i = 1

    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1

        elif length != 0:
            length = lps[length - 1]

        else:
            lps[i] = 0
            i += 1

    return lps


def kmp_search(text, pattern):
    n = len(text)
    m = len(pattern)

    lps = compute_lps(pattern)

    matches = []
    comparisons = 0

    i = 0
    j = 0

    while i < n:
        comparisons += 1

        if pattern[j] == text[i]:
            i += 1
            j += 1

            if j == m:
                matches.append(i - j)
                j = lps[j - 1]

        else:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

    return matches, comparisons


# ---------------- Rabin-Karp ----------------

def rabin_karp(text, pattern, q=101):
    n = len(text)
    m = len(pattern)

    if m > n:
        return [], 0

    d = 256

    h = pow(d, m - 1, q)

    p_hash = 0
    t_hash = 0

    matches = []
    comparisons = 0

    for i in range(m):
        p_hash = (d * p_hash + ord(pattern[i])) % q
        t_hash = (d * t_hash + ord(text[i])) % q

    for s in range(n - m + 1):

        if p_hash == t_hash:

            for k in range(m):
                comparisons += 1

                if text[s + k] != pattern[k]:
                    break
            else:
                matches.append(s)

        if s < n - m:
            t_hash = (
                d * (t_hash - ord(text[s]) * h)
                + ord(text[s + m])
            ) % q

            if t_hash < 0:
                t_hash += q

    return matches, comparisons


# ---------------- Streamlit App ----------------

def main():

    st.set_page_config(
        page_title="String Matching Algorithms",
        page_icon="🔍",
        layout="wide"
    )

    st.title("🔍 String Matching Algorithms Comparison")

    st.markdown("""
    Compare the performance of:

    - Naive Search
    - KMP (Knuth-Morris-Pratt)
    - Rabin-Karp
    """)

    text = st.text_area(
        "Enter Text",
        value="AABAACAADAABAABA",
        height=150
    )

    pattern = st.text_input(
        "Enter Pattern",
        value="AABA"
    )

    if st.button("Search Pattern"):

        if pattern.strip() == "":
            st.error("Pattern cannot be empty.")

        else:

            n_match, n_comp = naive_search(text, pattern)
            k_match, k_comp = kmp_search(text, pattern)
            r_match, r_comp = rabin_karp(text, pattern)

            st.subheader("Search Results")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.success("Naive Search")
                st.write("Matches:", n_match)
                st.write("Comparisons:", n_comp)

            with col2:
                st.info("KMP Search")
                st.write("Matches:", k_match)
                st.write("Comparisons:", k_comp)

            with col3:
                st.warning("Rabin-Karp Search")
                st.write("Matches:", r_match)
                st.write("Comparisons:", r_comp)

    st.divider()

    st.subheader("Performance Test")

    st.write(
        "Generate a random text of length 10,000 and compare algorithm efficiency."
    )

    if st.button("Run Performance Test"):

        text_large = ''.join(
            random.choices('ABCD', k=10000)
        )

        patterns = [
            'AB',
            'ABCD',
            'ABCDAB',
            'ABCDABCD'
        ]

        results = []

        for p in patterns:

            _, naive_comp = naive_search(text_large, p)
            _, kmp_comp = kmp_search(text_large, p)
            _, rk_comp = rabin_karp(text_large, p)

            results.append({
                "Pattern": p,
                "Naive Comparisons": naive_comp,
                "KMP Comparisons": kmp_comp,
                "Rabin-Karp Comparisons": rk_comp
            })

        df = pd.DataFrame(results)

        st.dataframe(
            df,
            use_container_width=True
        )

        st.bar_chart(
            df.set_index("Pattern")
        )

        st.success("Performance comparison completed.")


if __name__ == "__main__":
    main()