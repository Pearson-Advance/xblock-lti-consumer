PADV-412: LTI 1.3 Pluggable and re-usable LTI configuration
===========================================================

Status
======

Proposal

Context
=======

In this discovery, we will describe a possible approach to add LTI 1.3 support
for pluggable and re-usable LTI configurations on the lti_store plugin and
xblock-lti-consumer XBlock.

The #239 issue on xblock-lti-consumer [4]_ added support for LTI 1.1
pluggability, on the Open edX roadmap ticket #143 [1]_, related to the feature
of external pluggable LTI configuration, there was planned implementation for
LTI 1.3 support, according to comments on #210 [3]_, progress on this effort
has been stopped, currently, the remaining efforts to reach LTI 1.3 support are:

- Expand the plugin support to allow storing and retrieval of LTI 1.3
  configuration
- Update the LTI Consumer to use the configuration from the filter pipeline to
  load an external LTI tool using LTI 1.3 spec
- Remove XBlock dependencies from LTI 1.3 launches (features related to LTI 1.3
  authentication, for example, the keyset URL and the token URL).

Why do we need this?
====================

This feature is important because it will allow us to eliminate the need to
configure multiple LTI tools for each LTI 1.3 consumer XBlock (course authors
may not have access to deploy LTI 1.3 tools) and allow LTI 1.3 consumer XBlock
to share a common configuration, this will also allow for multi-tenancy model
compatibility on the platform and ease the maintenance of courses that heavily
depend on many LTI 1.3 XBlocks. We will also be able to use CCX XBlocks that
use LTI 1.3 since the CCX XBlocks would not have a separate configuration from
its master course counterpart.

General Approach
===============

We will need to modify the lti_store plugin and xblock-lti-consumer to include
these changes:

Changes on xblock-lti-consumer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Modify xblock-lti-consumer to allow setting the
  "LTI Reusable Configuration ID" field and add the "Reusable Configuration"
  option to the "Configuration Type" field on XBlocs using LTI 1.3 version.
- Modify the _get_lti_1p3_consumer method on the LTI configuration model to use
  the values from the external configuration when enabled.
- Modify the get_lti_1p3_launch_info function to show the values from the
  external configuration on the author view.

Changes on lti_store
~~~~~~~~~~~~~~~~~~~~

- Add an LTI 1.3 external configuration model to lti_store with fields for the
  client ID, private key, private key ID, public key or keyset URL, and
  optionally the deployment id.
- Add the LTI 1.3 external configuration model to the admin view and display
  the name, slug, token URL, keyset URL, and filter key.
- Add an access token view to lti_store for LTI 1.3 external configurations.
- Add a keyset view to lti_store for LTI 1.3 external configurations.
- Modify the lti_store pipeline GetLtiConfigurations to also include LTI 1.3
  external configurations in the result.

Note: The private key ID on the LTI 1.3 external configuration model can be an
auto-generated uuid4, just as how it's already being done on the
_generate_lti_1p3_keys_if_missing method on the LtiConfiguration model in
xblock-lti-consumer.

References
==========

.. [1] #143 Open edX Roadmap - Central Management of LTI Configuration: https://github.com/openedx/platform-roadmap/issues/143
.. [2] Pluggable and re-usable LTI configuration ADR: https://github.com/openedx/xblock-lti-consumer/blob/469d47dd2b3f1f742da429a64108b5a4ff03165d/docs/decisions/0006-pluggable-lti-configuration.rst
.. [3] #210 Pluggable/reusable LTI configuration: https://github.com/openedx/xblock-lti-consumer/pull/210
.. [4] #239 Support for external LTI configurations using openedx-filters: https://github.com/openedx/xblock-lti-consumer/pull/239
.. [5] Openedx LTI Store: https://github.com/open-craft/openedx-ltistore
