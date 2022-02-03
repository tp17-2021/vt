<script>
    export let text = "";
    // import 'node_modules/@id-sk/frontend/idsk/components/button/button.js';
</script>

<style type="text/scss">
  @import 'node_modules/@id-sk/frontend/govuk/components/button/_button';

  /*TODO: for some reason .govuk-button--secondary isn't imported from @id-sk*/
  .govuk-button--secondary {
    background-color: #dddddd;
    color: black;
  }
  .govuk-button {
    margin-bottom: 0 !important;
  }

</style>

<button name="secondary" type="submit" class="govuk-button govuk-button--secondary" data-module="govuk-button" on:click>
    {text}<slot />
</button>