<script>
    import SecondaryButton from "./buttons/SecondaryButton.svelte";
    import PrimaryButton from "./buttons/PrimaryButton.svelte";

    let visible = false;
    export let title = "";
    export let subtitle = "";

    export function closeModal() {
        visible = false;
    }

    export function openModal() {
        visible = true;
    }

    export let yesCallback = null;

    export let yesTxt = "Potvrdiť";
    export let cancelTxt = "Zrušiť";
    export let okTxt = "Rozumiem";
</script>

<style lang="scss">
  .title {
    font-size: 2rem;
    font-weight: bold;
    margin-bottom: 1rem;
  }

  .subtitle {
    font-size: 1.5rem;
    font-weight: bold;
    margin-bottom: 1rem;
  }

  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    z-index: 10;
    backdrop-filter: blur(3px);
  }

  .modal-content {
    border: 5px solid #000000;
    border-top: 33px solid #000000;
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 90%;
    max-width: 1000px;
    background-color: #fff;
    padding: 20px;
    z-index: 11;
  }

  .cancelYes {
    margin-top: 2rem;
    display: flex;
    justify-content: end;
    gap: 1rem;
  }
</style>

{#if visible}
    <div>
        <div class="modal-overlay" on:click={()=>closeModal()}></div>
        <div class="modal-content">
            {#if $$slots.title}
                <span class="title"><slot name="title"/></span>
            {/if}
            {#if $$slots.subtitle}
                <span class="subtitle"><slot name="subtitle"/></span>
            {/if}
            <slot></slot>
            {#if yesCallback !== null}
                <div class="cancelYes">
<!--                    confirm / cancel choice-->
                    <SecondaryButton on:click={()=>closeModal()}>{cancelTxt}</SecondaryButton>
                    <PrimaryButton on:click={()=>yesCallback()}>{yesTxt}</PrimaryButton>
                </div>
            {:else}
<!--                else show only one button 'alert'-->
                <PrimaryButton on:click={()=>closeModal()}>{okTxt}</PrimaryButton>
            {/if}
        </div>
    </div>
{/if}
