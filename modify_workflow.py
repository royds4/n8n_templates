import json

with open("BTC Scrapping.json", "r") as f:
    data = json.load(f)

for node in data["nodes"]:
    if node["name"] == "Top & Bottom Watchout1":
        content = node["parameters"]["messages"]["values"][0]["content"]
        # Remove '=' prefix and standard context insertion for the clean block
        clean_content = content.replace('=', '', 1).replace('{{ JSON.stringify($json, null, 2) }}', '').strip()
        new_content = f"""=<role>
You are an institutional quantitative analyst.
</role>

<rules>
- You must only use the provided data.
- You must output strict JSON without markdown code blocks.
- You must not hallucinate.
</rules>

<context>
{clean_content}

{{{{ JSON.stringify($json, null, 2) }}}}
</context>

<planning_process>
Explicitly state your step-by-step reasoning inside this tag BEFORE generating the final output. Think about the cycle metrics, risk context, and synthesize the conclusion.
</planning_process>

<task>
Output EXACTLY this JSON structure:
{{
  "title": "Top & Bottom Watchout",
  "analysis": "..."
}}
</task>"""
        node["parameters"]["messages"]["values"][0]["content"] = new_content

    elif node["name"] == "BTC Meso Market Analysis1":
        content = node["parameters"]["messages"]["values"][0]["content"]
        clean_content = content.replace('=', '', 1).replace('{{ JSON.stringify($json, null, 2) }}', '').split('Output EXACTLY this structure')[0].strip()

        new_content = f"""=<role>
You are an institutional quantitative analyst.
</role>

<rules>
- You must only use the provided data.
- You must output strict JSON without markdown code blocks.
- You must not hallucinate.
</rules>

<context>
{clean_content}

{{{{ JSON.stringify($json, null, 2) }}}}
</context>

<planning_process>
Explicitly state your step-by-step reasoning inside this tag BEFORE generating the final output. Extract the required data points, evaluate the trends, and formulate the summary.
</planning_process>

<task>
Output EXACTLY this JSON structure:
{{
  "title": "BTC Meso Market Analysis",
  "mesoBrief": {{
    "Price & Trend": "...",
    "Momentum": "...",
    "Cycle (S2F & Rainbow)": "...",
    "On-chain/Issuance": "...",
    "Dominance & Rotation": "...",
    "Levels": {{
      "Support": "...",
      "Resistance": "..."
    }},
    "Outlook": {{
      "2-4 weeks": "...",
      "3-6 months": "..."
    }}
  }},
  "triggers": {{
    "Bull": "...",
    "Bear": "..."
  }},
  "mesoBias": "mildly-bullish | neutral | mildly-bearish",
  "horizon": ["weeks", "months"]
}}
</task>"""
        node["parameters"]["messages"]["values"][0]["content"] = new_content

    elif node["name"] == "Micro Market Analysis":
        content = node["parameters"]["messages"]["values"][0]["content"]
        clean_content = content.replace('=', '', 1).replace('{{ JSON.stringify($json, null, 2) }}', '').strip()

        new_content = f"""=<role>
You are an institutional quantitative analyst.
</role>

<rules>
- You must only use the provided data.
- You must output strict JSON without markdown code blocks.
- You must not hallucinate.
</rules>

<context>
{clean_content}

{{{{ JSON.stringify($json, null, 2) }}}}
</context>

<planning_process>
Explicitly state your step-by-step reasoning inside this tag BEFORE generating the final output. Identify the micro-level indicators and summarize them factually.
</planning_process>

<task>
Output EXACTLY this JSON structure:
{{
  "title": "BTC Micro Market Analysis",
  "indicators": {{
    "funding_rate": "...",
    "open_interest": "...",
    "volatility_squeeze": "...",
    "...": "..."
  }},
  "summary": "..."
}}
</task>"""
        node["parameters"]["messages"]["values"][0]["content"] = new_content

    elif node["name"] == "Market Stance1":
        content = node["parameters"]["messages"]["values"][0]["content"]
        # Extract everything up to Instructions
        clean_content = content.replace('=', '', 1).split('CRITICAL HTML RULES')[0].strip()

        # We need to manually construct context because of splitting logic
        context_data_str = """Input Data:
QUANT_BRAIN (Source of Truth):
Signal: {{ $json.signal }}
Risk Score: {{$json.risk_score}}/100
Headline: {{$json.headline}}
Trade Setup: {{JSON.stringify($json.trade_setup)}}
Rationale: {{$json.report_markdown}}
METRICS:
{{JSON.stringify($('Data Clean and Debug').item.json.metrics)}}

ANALYSIS SUMMARIES:
{{$('Data Clean and Debug').item.json.macro}}
{{$('Data Clean and Debug').item.json.meso}}
{{$('Data Clean and Debug').item.json.micro}}
{{$('Data Clean and Debug').item.json.topbottom}}

NEWS:
{{$('Data Clean and Debug').item.json.news}}"""

        instructions = content.split('Instructions:')[1].split('Output the result')[0].strip()

        new_content = f"""=<role>
You are an institutional quantitative analyst.
</role>

<rules>
- You must only use the provided data.
- You must not hallucinate.
- NEVER use the '&' character on its own. You MUST write it as '&amp;' every single time.
- Escape < and > as &lt; and &gt;.
- Do not use Markdown. Use only HTML tags (<b>, <i>, <code>).
- NEVER use <ul>, <li>, or <br> tags.
</rules>

<context>
{clean_content}

{context_data_str}

Instructions:
{instructions}
</context>

<planning_process>
Explicitly state your step-by-step reasoning inside this tag BEFORE generating the final output. Formulate the Tactical Stance, Analyst Rationale, and pick headlines while strictly following the HTML rules.
</planning_process>

<task>
Output the result using this EXACT HTML template (do not change the structure, just fill the slots):

<b>📅 CRYPTO ANALYSIS</b> <i>{{{{$('Data Clean and Debug').item.json.metrics.date}}}}</i>

<b>🛑 CYCLE SIGNAL:</b> <b>{{{{$json.signal}}}}</b> (Score: {{{{$json.risk_score}}}})

➖➖➖➖➖➖➖➖➖➖➖

<b>🌊 MACRO &amp; LIQUIDITY</b> • <b>Regime:</b> {{{{$('Data Clean and Debug').item.json.metrics.macro_bias}}}} • <b>Liquidity:</b> {{{{$('Data Clean and Debug').item.json.metrics.liquidity_trend}}}} • <b>10Y Yield:</b> <code>{{{{$('Data Clean and Debug').item.json.metrics.yield10y}}}}</code>

<b>🔄 MESO &amp; ROTATION</b> • <b>Regime:</b> {{{{$('Data Clean and Debug').item.json.metrics.market_regime}}}} • <b>ETH/BTC:</b> <code>{{{{$('Data Clean and Debug').item.json.metrics.eth_btc_price}}}}</code>

<b>🔬 MICRO &amp; SENTIMENT</b> • <b>Funding:</b> <code>{{{{$('Data Clean and Debug').item.json.metrics.funding_rate}}}}</code> • <b>Fear &amp; Greed:</b> {{{{$('Data Clean and Debug').item.json.metrics.fear_greed_index}}}}

<b>⚖️ TOP &amp; BOTTOM</b> • <b>vs 200WMA:</b> <code>{{{{$('Data Clean and Debug').item.json.metrics.dist_to_200_wma}}}}%</code> • <b>Drawdown:</b> <code>{{{{$('Data Clean and Debug').item.json.metrics.drawdown_percent}}}}%</code>


➖➖➖➖➖➖➖➖➖➖➖

<b>🎯 TACTICAL STANCE</b> [Insert Your Escaped Tactical Stance Here. Include Trade Levels if available!]

<b>🧠 ANALYST RATIONALE</b> <i>[Insert Your Escaped Rationale Here]</i>

📰 <b>HEADLINES</b> [Insert Top 3 Headlines as bullet points. Ensure no naked '&' symbols exist here!]
</task>"""

        node["parameters"]["messages"]["values"][0]["content"] = new_content

    elif node["name"] == "Data Clean and Debug":
        jscode = node["parameters"]["jsCode"]
        new_jscode = jscode.replace("""function pickContent(d) {
    if (!d) return null;

    // 1. Google Gemini / PaLM (Structure: content.parts[0].text)
    if (d.content?.parts?.[0]?.text) {
        return d.content.parts[0].text;
    }""", """function pickContent(d) {
    if (!d) return null;

    let text = null;

    // 1. Google Gemini / PaLM (Structure: content.parts[0].text)
    if (d.content?.parts?.[0]?.text) {
        text = d.content.parts[0].text;
    }""")
        new_jscode = new_jscode.replace("""    // 2. OpenAI / Standard (Structure: choices[0].message.content)
    if (d.choices?.[0]?.message?.content) {
        return d.choices[0].message.content;
    }""", """    // 2. OpenAI / Standard (Structure: choices[0].message.content)
    else if (d.choices?.[0]?.message?.content) {
        text = d.choices[0].message.content;
    }""")
        new_jscode = new_jscode.replace("""    // 3. Direct Message (Anthropic/Other)
    if (d.message?.content) {
        return d.message.content;
    }""", """    // 3. Direct Message (Anthropic/Other)
    else if (d.message?.content) {
        text = d.message.content;
    }""")
        new_jscode = new_jscode.replace("""    // 4. Fallback: Content is already a simple string
    if (typeof d.content === 'string') {
        return d.content;
    }

    return null;
}""", """    // 4. Fallback: Content is already a simple string
    else if (typeof d.content === 'string') {
        text = d.content;
    } else if (typeof d === 'string') {
        text = d;
    }

    if (!text) return null;

    // Strip planning_process XML tag
    text = text.replace(/<planning_process>[\\s\\S]*?<\\/planning_process>/gi, '');

    // Strip JSON markdown wrapper
    text = text.replace(/^```json\\s*/i, '').replace(/```$/i, '').trim();

    return text;
}""")

        new_jscode = new_jscode.replace("""function classify(text) {
    if (!text || typeof text !== "string") return;
    const t = text.toLowerCase();

    if (!macro && (t.includes("macro market analysis") || t.startsWith("macro "))) {
        macro = text;
    } else if (!meso && (t.includes("meso market analysis") || t.includes("price & trend"))) {
        meso = text;
    } else if (!micro && (t.includes("micro market analysis") || t.includes("volatility squeeze"))) {
        micro = text;
    } else if (!news && (t.includes("crypto news summary") || t.includes("sentiment:"))) {
        news = text;
    } else if (!topbottom && (t.includes("top & bottom") || t.includes("cycle turning point"))) {
        topbottom = text;
    }
}""", """function classify(text) {
    if (!text || typeof text !== "string") return;

    // Attempt to parse as JSON first
    try {
        const parsed = JSON.parse(text);
        if (parsed.title) {
            const title = parsed.title.toLowerCase();
            if (title.includes("macro market analysis") && !macro) macro = text;
            else if (title.includes("meso market analysis") && !meso) meso = text;
            else if (title.includes("micro market analysis") && !micro) micro = text;
            else if (title.includes("top & bottom watchout") && !topbottom) topbottom = text;
            return;
        }
    } catch(e) {
        // Fallback to text matching if not valid JSON
    }

    const t = text.toLowerCase();

    if (!macro && (t.includes("macro market analysis") || t.startsWith("macro "))) {
        macro = text;
    } else if (!meso && (t.includes("meso market analysis") || t.includes("price & trend"))) {
        meso = text;
    } else if (!micro && (t.includes("micro market analysis") || t.includes("volatility squeeze"))) {
        micro = text;
    } else if (!news && (t.includes("crypto news summary") || t.includes("sentiment:"))) {
        news = text;
    } else if (!topbottom && (t.includes("top & bottom") || t.includes("cycle turning point"))) {
        topbottom = text;
    }
}""")

        node["parameters"]["jsCode"] = new_jscode

    elif node["name"] == "Send a text message":
        if "additionalFields" not in node["parameters"]:
            node["parameters"]["additionalFields"] = {}
        node["parameters"]["additionalFields"]["parse_mode"] = "HTML"

with open("BTC Scrapping_modified.json", "w") as f:
    json.dump(data, f, indent=2)
