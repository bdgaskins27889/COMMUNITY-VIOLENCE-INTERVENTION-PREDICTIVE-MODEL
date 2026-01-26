# CVI Risk Predictor: Ethical Framework and Safeguards

**Author:** Barbara D. Gaskins  
**Last Updated:** January 23, 2026

---

## 1. Guiding Philosophy: Prevention, Not Punishment

The CVI Risk Predictor is founded on a public health approach to violence prevention. Its sole purpose is to empower Community Violence Intervention (CVI) organizations with data-driven insights to support their life-saving work. Our methodology and technology are explicitly designed for **care-oriented intervention**, not for surveillance or law enforcement action. We believe that data, when applied ethically, can be a powerful tool for promoting community well-being and equity.

This framework outlines the principles and technical safeguards embedded in the project to ensure it is used responsibly and to mitigate the risks of harm associated with predictive technologies in the justice space.

---

## 2. Core Ethical Principles

| Principle                  | Commitment                                                                                                                                                           |
| -------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Community Benefit**      | The tool is designed exclusively to support the non-punitive, preventative missions of CVI organizations and public health bodies.                                       |
| **Rejection of Surveillance** | We explicitly reject and prevent the use of this tool for law enforcement surveillance, predictive policing, or any form of individual targeting.                      |
| **Transparency & Explainability** | The model's methodology, data sources, and limitations are openly documented. Predictions are accompanied by explanations to ensure they are not a "black box."         |
| **Privacy Protection**     | All analysis is conducted at an aggregated geographic level (e.g., neighborhood) to make the identification of individuals impossible.                                   |
| **Bias Awareness & Mitigation** | We acknowledge that all data is imperfect and can reflect historical biases. We are committed to identifying, documenting, and working to mitigate these biases.         |
| **Accountability**         | The tool is designed to augment, not replace, the professional judgment and lived experience of CVI practitioners. The ultimate responsibility for action rests with the user. |

---

## 3. Technical and Methodological Safeguards

These principles are not just ideals; they are enforced through concrete technical and methodological choices at every stage of the project.

### 3.1. Data Aggregation

-   **No Individual-Level Data:** The system never processes or stores data that can be tied to a specific person. All data is aggregated to the **neighborhood** or **census tract** level before analysis.
-   **Minimum Population Threshold:** Analytical units (neighborhoods) must meet a minimum population threshold (e.g., 500 residents) to be included. This prevents the possibility of de-anonymizing individuals in sparsely populated areas.
-   **Address Redaction:** Source data, such as crime reports, already has addresses redacted to the block level. Our system does not attempt to reverse this or derive specific addresses.

### 3.2. Model Design

-   **Focus on Place, Not People:** The model predicts the risk for a *place* (a neighborhood) during a *time period* (a week). It does **not** predict an individual's likelihood of committing or being a victim of violence.
-   **Interpretable Models:** The inclusion of Logistic Regression in our model suite ensures that we can provide clear explanations for why a neighborhood is flagged as high-risk. The feature importance scores from the Random Forest model further support this explainability.
-   **Exclusion of Law Enforcement Metrics:** The model is not trained on or optimized for metrics relevant to policing, such as arrest rates. The focus is on the incidence of violence as a public health indicator.

### 3.3. Data Bias Management

We recognize that crime data is not a perfect reflection of reality. It is a record of *reported* incidents and can be influenced by policing patterns and community trust in law enforcement. Our approach to managing this bias includes:

-   **Documentation:** We clearly document the source of all data and its known limitations in the `DATA_SOURCES.md` file and within the application itself.
-   **Multi-Source Triangulation:** By integrating data from multiple sources (crime reports, ShotSpotter, 311 calls, census data), we reduce reliance on any single, potentially biased dataset.
-   **Focus on Violent Crime:** The model primarily focuses on serious violent crimes (e.g., homicide, assault, robbery), which tend to have higher reporting rates across different communities compared to lower-level offenses, partially mitigating reporting bias.

---

## 4. Intended and Prohibited Use

Clarity on the intended use of this tool is paramount.

### ✅ Intended Use Cases

-   **Strategic Planning:** CVI organizations can use the risk tiers (Low, Moderate, High, Critical) to develop long-term staffing and resource allocation plans.
-   **Proactive Outreach:** Identifying neighborhoods with emerging risk trends can help teams schedule proactive outreach and mediation efforts before violence escalates.
-   **Justifying Funding:** The data-driven risk assessments can be used in grant applications and reports to demonstrate need and justify requests for funding.
-   **Collaboration:** The tool can facilitate collaboration between CVI groups, public health departments, and other community stakeholders by providing a common, data-informed operating picture.

### ❌ Prohibited Use Cases

**This tool is explicitly NOT to be used for:**

-   **Predictive Policing:** It should never be used to direct police patrols or to justify increased police presence in a community.
-   **Individual Risk Scoring:** The model is technically incapable of and ethically opposed to assigning a risk score to any individual.
-   **Criminal Investigations:** The data and predictions are not suitable for use as evidence in any criminal proceeding.
-   **Any Form of Punitive Action:** The tool's outputs should never be used as a basis for arrest, citation, or any other punitive measure.

---

## 5. Conclusion: A Tool for Empowerment

The CVI Risk Predictor is an experiment in ethical AI for social good. It is built on the belief that technology can serve community-led safety initiatives without replicating the harms of a surveillance-based society. By adhering to this ethical framework, we aim to provide a tool that empowers CVI practitioners, respects community privacy, and contributes to a more just and peaceful future.
