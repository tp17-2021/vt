<script>
    export let text = "";
    // import 'node_modules/@id-sk/frontend/idsk/components/button/button.js';
</script>

<style type="text/scss">
  @import 'node_modules/@id-sk/frontend/govuk/components/button/_button';

  .govuk-button {
    margin-bottom: 0 !important;
  }
</style>

<button class="govuk-button" data-module="govuk-button" on:click>
    {text}<slot />
</button>