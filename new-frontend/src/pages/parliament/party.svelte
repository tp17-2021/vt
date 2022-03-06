<script lang="ts">
    import PartyBox from "../../lib/components/PartyBox.svelte";

    import Button from "../../lib/components/buttons/Button.svelte";
    import {parties, vote} from "../../api/stores";
    import {goto, url} from "@roxi/routify";

    $: console.log($parties);

    function chooseParty(party) {
        if (party == null) {
            $vote.party_id = null;
        }
        else {
            $vote.party_id = party._id;
        }
    }

    $: console.log("$vote.party_id", $vote.party_id);

    function next() {
        if ($vote.party_id == null) {
            $goto("/parliament/confirm/");
        }
        else    {
            $goto("/parliament/candidates/");
        }
    }
    
</script>

<!-- <Search
    title="Kandidujúce strany:"
    bind:filter
    placeholder="Vyhľadajte stranu"
/> -->
<h2>Kandidujúce strany:</h2>
<i>Kliknutím označte stranu, ktorú chcete voliť.</i>
<div class="parties">
    {#each $parties as party}
        <div on:click={() => chooseParty(party._id === $vote.party_id ? null : party)}>
            <PartyBox
                    {party}
                    isSelected={party._id === $vote.party_id}
                    showCheckbox={true}
                    }
            />
        </div>

    {/each}
</div>
<Button on:click={next}>Potvrdiť</Button>


<!--<Button >-->
<!-- 


<Pagination
    itemsCount={filtered.length}
    itemsPerPage={perPage}
    bind:currentPage
/>

<div class="nextBtn">
    <PrimaryButton text="Potvrdiť" on:click={openModal} />
</div>
{#if $chosenParty !== null}
    <Modal
        bind:openModal
        yesCallback={() => chooseCandidates()}
        yesTxt="Potvrdiť"
        cancelTxt="Upraviť"
    >
        <span slot="title">Zvolili ste</span>
        <PartyBox party={$chosenParty} />
    </Modal>
{:else}
    <Modal
        bind:openModal
        yesCallback={() => chooseCandidates()}
        yesTxt="Odoslať prázdny hlas"
        cancelTxt="Upraviť"
    >
        <span slot="title">Nezvolili ste žiadnu stranu</span>
        <span slot="subtitle">Naozaj chcete odoslať prázdny hlas?</span>
    </Modal>
{/if} -->
