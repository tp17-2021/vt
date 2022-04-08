<script lang="ts">
    import Checkbox from "./Checkbox.svelte";

    export let isSelected: boolean = false;
    export let party;

    export let showCheckbox: boolean = false;
</script>

<style lang="scss">
  .party {
    display: grid;
    grid-template-columns: 30px 150px 1fr;
    gap: 10px;
    align-content: center;
    background-color: var(--lightgray);
    align-items: center;
    padding: 10px 10px 10px 20px;
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 5px;

    &.withCheckbox {
      grid-template-columns: 60px 30px 150px 1fr;
    }

    img {
      width: 150px;
      height: auto;
    }

    &.chosen {
      background-color: var(--yellow);
    }
  }
</style>

<div class="party {isSelected ? 'chosen' : ''} {showCheckbox ? 'withCheckbox' : ''}" on:click >
    {#if showCheckbox}
        <div>
            <Checkbox bind:checked={isSelected} size={60} />
        </div>
    {/if}
    <div>{party.party_number}</div>
    <div>
        <img src="data:image/png;base64, {party.image_bytes}" alt="" />
    </div>
    <div>{party.name}</div>
</div>