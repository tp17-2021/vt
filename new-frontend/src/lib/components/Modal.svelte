<script>
    import Button from "./buttons/Button.svelte";
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
    margin-bottom: 2rem;
  }
  .subtitle {
    font-size: 1.5rem;
    margin-bottom: 2rem;
  }
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    z-index: 10;
    backdrop-filter: blur(6px);
  }
  .modal-content {
    border: 5px solid #000000;
    border-top: 33px solid #000000;
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background-color: #fff;
    z-index: 11;
    padding: 1rem;
    width: calc(100% - 2*2rem);
    max-width: calc(768px - 2* 2rem);
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
        <div class="modal-overlay" on:click={closeModal}></div>
        <div class="modal-content">
            {#if $$slots.title}
                <div class="title"><slot name="title"/></div>
            {/if}
            {#if $$slots.subtitle}
                <div class="subtitle"><slot name="subtitle"/></div>
            {/if}
            <slot></slot>
            {#if yesCallback !== null}
                <div class="cancelYes">
                    <!-- confirm / cancel choice-->
                    <Button on:click={closeModal}>{cancelTxt}</Button>
                    <Button on:click={yesCallback} type="primary">{yesTxt}</Button>
                </div>
            {:else}
                <!--                else show only one button 'alert'-->
                <Button on:click={closeModal} type="primary">{okTxt}</Button>
            {/if}
        </div>
    </div>
{/if}