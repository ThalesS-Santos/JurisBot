# Gemini Models Documentation - Text Focused

## Our Most Intelligent Model

### Gemini 3 Pro
The best model in the world for multimodal understanding, and our most powerful agentic and vibe-coding model yet, delivering richer visuals and deeper interactivity, all built on a foundation of state-of-the-art reasoning.

**Model Details**
| Property | Description |
|---|---|
| Model code | `gemini-3-pro-preview` |
| Supported data types | **Inputs:** Text, Image, Video, Audio, and PDF <br> **Output:** Text |
| Token limits | **Input:** 1,048,576 <br> **Output:** 65,536 |
| Capabilities | **Audio generation:** Not supported <br> **Batch API:** Supported <br> **Caching:** Supported <br> **Code execution:** Supported <br> **File search:** Supported <br> **Function calling:** Supported <br> **Grounding with Google Maps:** Not supported <br> **Image generation:** Not supported <br> **Live API:** Not supported <br> **Search grounding:** Supported <br> **Structured outputs:** Supported <br> **Thinking:** Supported <br> **URL context:** Supported |
| Latest update | November 2025 |
| Knowledge cutoff | January 2025 |

---

## Our Most Balanced Model

### Gemini 3 Flash
Our most balanced model built for speed, scale, and frontier intelligence.

**Model Details**
| Property | Description |
|---|---|
| Model code | `gemini-3-flash-preview` |
| Supported data types | **Inputs:** Text, Image, Video, Audio, and PDF <br> **Output:** Text |
| Token limits | **Input:** 1,048,576 <br> **Output:** 65,536 |
| Capabilities | **Audio generation:** Not supported <br> **Batch API:** Supported <br> **Caching:** Supported <br> **Code execution:** Supported <br> **File search:** Supported <br> **Function calling:** Supported <br> **Grounding with Google Maps:** Not supported <br> **Image generation:** Not supported <br> **Live API:** Not supported <br> **Search grounding:** Supported <br> **Structured outputs:** Supported <br> **Thinking:** Supported <br> **URL context:** Supported |
| Latest update | December 2025 |
| Knowledge cutoff | January 2025 |

---

## Fast and Intelligent

### Gemini 2.5 Flash
Our best model in terms of price-performance, offering well-rounded capabilities. 2.5 Flash is best for large scale processing, low-latency, high volume tasks that require thinking, and agentic use cases.

**Model Details**
| Property | Description |
|---|---|
| Model code | `gemini-2.5-flash` (Stable) <br> `gemini-2.5-flash-preview-09-2025` (Preview) |
| Supported data types | **Inputs:** Text, images, video, audio <br> **Output:** Text |
| Token limits | **Input:** 1,048,576 <br> **Output:** 65,536 |
| Capabilities | **Audio generation:** Not supported <br> **Batch API:** Supported <br> **Caching:** Supported <br> **Code execution:** Supported <br> **File search:** Supported <br> **Function calling:** Supported <br> **Grounding with Google Maps:** Supported (Stable only) <br> **Search grounding:** Supported <br> **Structured outputs:** Supported <br> **Thinking:** Supported <br> **URL context:** Supported |
| Latest update | June/September 2025 |
| Knowledge cutoff | January 2025 |

---

## Ultra Fast

### Gemini 2.5 Flash-Lite
Our fastest flash model optimized for cost-efficiency and high throughput.

**Model Details**
| Property | Description |
|---|---|
| Model code | `gemini-2.5-flash-lite` (Stable) <br> `gemini-2.5-flash-lite-preview-09-2025` (Preview) |
| Supported data types | **Inputs:** Text, image, video, audio, PDF <br> **Output:** Text |
| Token limits | **Input:** 1,048,576 <br> **Output:** 65,536 |
| Capabilities | **Audio generation:** Not supported <br> **Batch API:** Supported <br> **Caching:** Supported <br> **Code execution:** Supported <br> **File search:** Supported <br> **Function calling:** Supported <br> **Grounding with Google Maps:** Supported (Stable only) <br> **Search grounding:** Supported <br> **Structured outputs:** Supported <br> **Thinking:** Supported <br> **URL context:** Supported |
| Latest update | July/September 2025 |
| Knowledge cutoff | January 2025 |

---

## Advanced Thinking Model

### Gemini 2.5 Pro
Our state-of-the-art thinking model, capable of reasoning over complex problems in code, math, and STEM, as well as analyzing large datasets, codebases, and documents using long context.

**Model Details**
| Property | Description |
|---|---|
| Model code | `gemini-2.5-pro` |
| Supported data types | **Inputs:** Audio, images, video, text, and PDF <br> **Output:** Text |
| Token limits | **Input:** 1,048,576 <br> **Output:** 65,536 |
| Capabilities | **Audio generation:** Not supported <br> **Batch API:** Supported <br> **Caching:** Supported <br> **Code execution:** Supported <br> **File search:** Supported <br> **Function calling:** Supported <br> **Grounding with Google Maps:** Supported <br> **Search grounding:** Supported <br> **Structured outputs:** Supported <br> **Thinking:** Supported <br> **URL context:** Supported |
| Latest update | June 2025 |
| Knowledge cutoff | January 2025 |

---

## Previous Models

### Gemini 2.0 Flash
Our second generation workhorse model, with a 1 million token context window.

**Model Details**
| Property | Description |
|---|---|
| Model code | `gemini-2.0-flash` <br> `gemini-2.0-flash-001` (Stable) <br> `gemini-2.0-flash-exp` (Experimental) |
| Supported data types | **Inputs:** Audio, images, video, and text <br> **Output:** Text |
| Token limits | **Input:** 1,048,576 <br> **Output:** 8,192 |
| Capabilities | **Thinking:** Experimental <br> **File search:** Not supported <br> **URL context:** Not supported |
| Latest update | February 2025 |
| Knowledge cutoff | August 2024 |

### Gemini 2.0 Flash-Lite
A Gemini 2.0 Flash model optimized for cost efficiency and low latency.

**Model Details**
| Property | Description |
|---|---|
| Model code | `gemini-2.0-flash-lite` <br> `gemini-2.0-flash-lite-001` (Stable) |
| Supported data types | **Inputs:** Audio, images, video, and text <br> **Output:** Text |
| Token limits | **Input:** 1,048,576 <br> **Output:** 8,192 |
| Latest update | February 2025 |
| Knowledge cutoff | August 2024 |

---

## Model Version Name Patterns

Gemini models are available in either *stable*, *preview*, *latest*, or *experimental* versions.

### Stable
Points to a specific stable model. Stable models usually don't change. Most production apps should use a specific stable model.
*Example:* `gemini-2.5-flash`

### Preview
Points to a preview model which may be used for production. Preview models will typically have billing enabled, might come with more restrictive rate limits and will be deprecated with at least 2 weeks notice.
*Example:* `gemini-2.5-flash-preview-09-2025`

### Latest
Points to the latest release for a specific model variation. This can be a stable, preview or experimental release. This alias will get hot-swapped with every new release of a specific model variation. A **2-week notice** will be provided through email before the version behind latest is changed.
*Example:* `gemini-flash-latest`

### Experimental
Points to an experimental model which will typically be not be suitable for production use and come with more restrictive rate limits. We release experimental models to gather feedback and get our latest updates into the hands of developers quickly.
