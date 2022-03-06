<script lang="ts">
    import PartyBox from "../../lib/components/PartyBox.svelte";

    import Button from "../../lib/components/buttons/Button.svelte";
    import {parties, vote} from "../../api/stores";
    import {goto, url} from "@roxi/routify";
    import {get} from "svelte/store";
    import type {IpaginationObject} from "../../lib/components/pagination/paginate";
    import {searchAndPaginate} from "../../lib/components/pagination/paginate";
    import PaginationLinks from "../../lib/components/pagination/PaginationLinks.svelte";

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

    // // --- pagination and search ---
    let paginationObject: IpaginationObject = {
        items: get(parties),
        paginatedItems: [],
        searchTerm: "",
        currentPageNumber: 1,
        countOfPages: 1,
        itemsPerPage: 5,
        searchBy: ["name"],
    }
    let paginatedParties = []
    function paginateParties() {
        searchAndPaginate(paginationObject)  // paginationObject is updated inside this function
        paginatedParties = paginationObject.paginatedItems
    }
    
</script>

<style>
    .parties {
        height: calc(100vh - 500px);
    }
</style>

<h2>Kandidujúce strany:</h2>

<!--    search input -->
<input type="text" id="search" placeholder="Vyhľadajte kandidujúcu stranu" on:input={e => {
    paginationObject.currentPageNumber = 1
    paginationObject.searchTerm = e.target.value
    paginateParties(paginationObject)
}}>

<i>Kliknutím označte stranu, ktorú chcete voliť.</i>
<div class="parties">
    {#each paginatedParties as party}
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
<PaginationLinks paginationObject={paginationObject} paginationObjectChanged={paginateParties}/>
<Button on:click={next} type="primary">Potvrdiť</Button>


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
