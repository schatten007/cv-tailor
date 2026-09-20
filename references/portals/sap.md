# SAP SuccessFactors portal adapter

Identify SAP from observable application/provider evidence, not the employer's
industry. Tenants can have different domains, languages, account policies,
sections, attachments, screening questions, and Quick Apply configurations.
There is no one universal SAP candidate login or fixed sequence of clicks.

1. Follow the specific vacancy's application link. Confirm job reference and
   employer after redirects and sign-in; job search, talent registration, and an
   actual job application can look similar.
2. Reuse that employer's session. Handle existing account, new account, social
   sign-in, verification, or simplified/Quick Apply as shown. Ask before signup;
   credentials and MFA remain a browser handoff.
3. Distinguish candidate-profile fields from vacancy-specific application fields.
   Changes to a shared candidate profile may affect other applications: show
   substantive changes before replacing existing confirmed values.
4. Inspect each expandable subsection/wizard step. Add employment and education
   entries with their true dates; respect country/date/phone formats. Snapshot
   again after dependent dropdowns or Add/Save actions.
5. If CV parsing populates fields, check name, contact, title, employer, dates,
   degree, and language. Fix errors; do not assume a verification screen exists.
6. Check attachments at both profile and application levels. A CV uploaded to
   the profile may still need selecting for the specific vacancy. Confirm its
   actual displayed filename. Supporting fields may accept multiple documents
   or one merged PDF; apply the field's constraints, not a universal size limit.
7. Finish all observed sections and stop at the action that sends this vacancy's
   application. `Save`, `Next`, `Apply`, and translated labels are contextual;
   never treat the label alone as permission to submit.

After expiry or manual handoff re-open the intended vacancy/draft, re-inspect,
and reverify what is actually present. A local checkpoint is not proof of remote
persistence. Check for an existing application before beginning another.

Sources (configuration context, not tested customer-portal selectors):
- https://help.sap.com/docs/successfactors-recruiting/setting-up-and-maintaining-sap-successfactors-recruiting/create-external-candidate-account
- https://help.sap.com/doc/eb8c64b57d5c449e8c7284216a1b6094/2405/en-US/Recruiting_in_SAP_SuccessFactors_Test_Script_FC1.pdf
