<svelte:head>
    <link rel="stylesheet" href="https://pro.fontawesome.com/releases/v5.10.0/css/all.css"
          integrity="sha384-AYmEC3Yw5cVb3ZcuHtOA93w35dYTsvhLPVnYs9eStHfGJvOvKxVfELGroGkvsg+p" crossorigin="anonymous"/>
</svelte:head>

<style lang="scss" global>
  @import "scss/bootstrap";
</style>

<script>
    import {Router} from 'svelte-router-spa'
    import {routes} from "./routes";
    import {configIsLoading} from "./stores";
    import Debug from "./pages/Debug.svelte";
</script>

<!--don't render the page without loaded config-->
{#if !$configIsLoading}
    <div>
        <Router {routes}/>
    </div>
    <Debug/>
{/if}
