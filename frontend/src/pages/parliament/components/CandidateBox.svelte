<script lang="ts">
    import Checkbox from "../../../components/Checkbox.svelte";

    export let isSelected: boolean = false;
    export let candidate;
    export let showCheckbox: boolean = false;
</script>

<style lang="scss">
  .candidate {
    display: grid;
    grid-template-columns: 20fr 5fr 7fr 15fr 7fr;
    gap: 10px;

    align-items: center;

    padding: .6rem 2rem;
    margin: 5px 0;
    background-color: var(--lightgray);

    &.withCheckbox {
      grid-template-columns: 40px 20fr 5fr 7fr 15fr 7fr;
    }

    .name {
      font-size: 1.25rem;
      font-weight: bold;
    }

    &.chosen {
      //border: 4px solid var(--yellow);
      //margin: 1px -4px; // top/bottom = 5px original - 4px border = 1 px; left/right = -4px border
      background-color: var(--yellow);
    }
  }
</style>

<div class="candidate {isSelected ? 'chosen' : ''} {showCheckbox ? 'withCheckbox' : ''}" on:click>
    {#if showCheckbox}
        <div>
            <Checkbox checked={isSelected} size={40}/>
        </div>
    {/if}
    <span class="name">{candidate.id}. {candidate.name}</span>
    <span>{candidate.degree}</span>
    <span>{candidate.age} rokov</span>
    <span>{candidate.profession}</span>
    <span>{candidate.city}</span>
</div>