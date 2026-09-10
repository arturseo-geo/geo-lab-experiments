# E097 page body, FINAL (AJ voice, 10 Sep 2026)
# Identical on both arms: /guides/hreflang-and-ai-search-explained and /guides/p48213
# Protocol: e097-e100-prereg-v1.2

**Title / H1:** Hreflang and AI search: which language version gets cited, and why

Hreflang tells Google which language and regional versions of a page belong together. But AI search engines were not built around hreflang, and there is no public evidence that they use it when choosing which page to cite.

What they clearly can use is the page itself, the language it is written in and whether that version exists in the index they search.

That creates a problem for multilingual sites. The setup that works well for Google, with hreflang clusters, regional canonicals and one URL per locale, does not necessarily carry across to AI answer engines.

Here is what we know, what we can reasonably infer and what still has not been properly tested.

## How AI search engines handle hreflang

Each engine retrieves sources differently, so hreflang sits at a different distance from the final citation decision.

Google AI Overviews use Google's own search index, where hreflang is already part of the indexing and ranking process. The language version cited in an AI Overview will usually be the one Google considers most appropriate for that user and location.

In that case, hreflang works upstream. It helps Google choose which version to rank, and the AI Overview inherits that choice.

ChatGPT Search, Perplexity and Gemini with grounding work differently. They retrieve candidate pages from their own indexes or search partners, then pass those pages into a system that decides which sources to use and cite.

Hreflang is a link relation inside the page's `<head>`. None of these engines has documented a citation-selection step that reads it. The more visible signal is the language of the page itself and how closely its text matches the query.

## Does hreflang affect which language version gets cited?

For Google AI Overviews, it may have an indirect effect because hreflang can influence what Google indexes and ranks.

For the other engines, there is no published evidence that hreflang itself affects citation selection. The version most likely to be cited is the one that matches the query language and was available in the engine's index at the time.

If a site has English and Spanish versions of the same article and the query is written in English, the English page is the natural candidate whether the pages belong to a hreflang cluster or not.

The problems begin when an engine has indexed only one version. If it crawled the German page but never found the English one, an English query may still produce a citation to the German page. Hreflang cannot help if the preferred page is missing from the index being searched.

## How AI assistants choose between translated pages

The clearest pattern we can observe is language match first, followed by the engine's normal source-selection process.

AI assistants generally cite pages written in the same language as the query. Where several versions use the same language, such as en-GB and en-US, the choice starts to look like an ordinary retrieval and ranking decision. Whichever version the engine surfaces most strongly is the one most likely to be cited.

There is currently no evidence that the model itself applies a separate regional preference based on hreflang.

That remains an inference from observed behaviour. The engines do not publicly describe a specific language-selection stage in enough detail to confirm it.

## Do you need hreflang for AI search visibility?

You still need hreflang for Google, and Google AI Overviews draw from Google Search.

For other AI engines, hreflang is neither a known requirement nor a proven citation advantage. What matters more is whether every language version can be crawled, indexed and clearly understood as being written in that language.

A page that mixes languages, keeps an untranslated title or relies on weak machine translation gives the retrieval system a less confident match than a clean, properly localised page.

The honest answer is simple: keep hreflang for the reasons you already use it, but do not expect the attribute alone to increase AI citations.

## How to optimise a multilingual website for AI search

There are four practical steps, and none is a hreflang trick.

1. **Use one clear language per URL.** Retrieval systems score the visible text. A page written consistently in one language is easier to match with queries in that language.

2. **Make every version crawlable.** If some locales block relevant search or AI crawlers while others do not, the engines may build an uneven picture of the site. Uneven index coverage leads to unexpected citations.

3. **Write the title and opening paragraph in the target language.** Name the topic directly. These prominent fields are likely to carry more retrieval value than a URL slug or a hreflang annotation.

4. **Avoid automatic geographic redirects.** If a crawler arriving from a US IP is immediately sent to the US version, it may never discover the other regional pages.

## Can AI search engines cite the wrong language version?

Yes. The most likely cause is incomplete index coverage, not necessarily a failure in citation selection.

If the engine has found only one language version, that is the only version it can cite.

Language ambiguity can create the same problem. Shared navigation in another language, mixed-language boilerplate, an untranslated title or a partially translated body can all make the page harder to classify.

The engine can only work with the pages and signals it was able to retrieve.

## Does AI search treat translated pages as duplicate content?

Google does not normally treat properly translated pages as duplicates when hreflang and canonicals are configured correctly. Google AI Overviews inherit that search-layer handling.

For other AI engines, "duplicate content" may be the wrong way to frame the question. Their retrieval systems are trying to find the text that best matches the query, not necessarily applying Google's duplicate-content rules.

Two well-translated pages contain different text in different languages, so they are distinct retrieval candidates.

A weak translation that leaves much of the original language in place is more ambiguous. It may compete with the original page for the same queries or be ignored in favour of the clearer version.

## Which URL gets cited when a page exists in several languages?

Usually, it will be the URL that matches the query language and is available in the engine's index.

If more than one URL meets both conditions, the engine's normal source-selection process decides between them. Based on what is currently observable, titles and visible page text are more likely to matter than hreflang.

## What has not been measured

Most of this guidance comes from documented retrieval behaviour and what we can observe in live results.

There is no controlled experiment on record that keeps the content fixed, changes only the hreflang setup or the language version available to the crawler, and then measures citation rates across engines.

Until that test exists, this should be treated as the safest working model, not a proven optimisation lever.
