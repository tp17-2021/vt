<script>
    import ImageScreen, {icons} from "../../lib/ImageScreen.svelte";
    import Button from "../../lib/components/buttons/Button.svelte";
    import {goto} from "@roxi/routify";

    function goHome() {
        $goto("/");
    }

</script>

<style>
    .pb-3 {
        padding-bottom: 1rem;
    }
</style>

<ImageScreen icon={icons.ERROR} title="Váš hlas nebol započítaný">
    <div class="pb-3">Nastala chyba, <b>prosím zavolajte obsluhu</b></div>
    <Button on:click={goHome}>
        <i class="fas fa-home"></i> Späť domov
    </Button>
</ImageScreen>