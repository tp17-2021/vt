<script>
import {isLoading} from "./spinner";
import ImageScreen, {icons} from "../../ImageScreen.svelte";
</script>
<style lang="scss">
  .spinnerScreen {
    display: grid;
    place-items: center;
    background-color: white;
    width: 100vw;
    height: 100vh;
    position: absolute;
    top: 0;
    left: 0;
    z-index: 999;
  }
</style>

{#if $isLoading}
    <div class="spinnerScreen">
        <ImageScreen title="Čakajte prosím" icon={icons.SPINNER}/>
    </div>
{/if}
