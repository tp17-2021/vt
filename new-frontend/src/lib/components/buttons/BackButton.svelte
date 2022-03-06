<script>
    import Button from "./Button.svelte";

    function navigateBack() {
        window.history.back();
    }
</script>

<style>
    .back-button-container {
        width: 100px;
    }
</style>
<div class="back-button-container">
    <Button on:click={()=>navigateBack()}>❮ späť</Button>
</div>
