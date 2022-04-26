<script lang="ts">
    import Checkbox from "./Checkbox.svelte";

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

    > span {
      /*clamp to 2 rows*/
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }

    &.chosen {
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
    <span class="name">{candidate.order}. {candidate.first_name} {candidate.last_name}</span>
    <span>{candidate.degrees_before}</span>
    <span>{candidate.age} rokov</span>
    <span>{candidate.occupation}</span>
    <span>{candidate.residence}</span>
</div>