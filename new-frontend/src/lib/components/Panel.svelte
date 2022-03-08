<script lang="ts">
    export let type = "confirmation";
    export let anchor = "";
</script>

<style type="text/scss">
    @import 'node_modules/@id-sk/frontend/govuk/components/panel/_panel';

    .govuk-panel--success {
        color: govuk-colour("white");
        background: govuk-colour("green");
    }

    .govuk-panel--danger {
        color: govuk-colour("white");
        background: govuk-colour("red");
    }

    .govuk-panel--warning {
        color: govuk-colour("white");
        background: govuk-colour("orange");
    }

</style>

<div id="{anchor}" class="govuk-panel govuk-panel--{type}">
    <slot></slot>
</div>
