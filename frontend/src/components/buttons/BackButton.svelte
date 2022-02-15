<script>
    import SecondaryButton from "./SecondaryButton.svelte";

    function navigateBack() {
        window.history.back();
    }
</script>
<SecondaryButton on:click={()=>navigateBack()}>Späť</SecondaryButton>