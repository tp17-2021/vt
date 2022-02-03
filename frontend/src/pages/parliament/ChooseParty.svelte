<script lang="ts">
    import {config, chosenParty} from "../../stores"
    import MainLayout from "../../parts/layouts/MainLayout.svelte"
    import PrimaryButton from "../../components/buttons/PrimaryButton.svelte"
    import Modal from "../../components/Modal.svelte"
    import {navigateTo} from "svelte-router-spa"
    import {filterCandidate} from "../../helpers/filter";
    import {paginate} from "../../helpers/pagination";
    import Pagination from "../../components/Pagination.svelte";
    import Search from "../../components/Search.svelte";
    import PartyBox from "./components/PartyBox.svelte";

    function chooseParty(party) {
        if (party?.id === $chosenParty?.id) {
            $chosenParty = null
        }
        else {
            console.log("chooseParty", party.id);
            $chosenParty = party
        }
    }

    function chooseCandidates() {
        if ($chosenParty === null) {
            navigateTo("/parliament/confirm")
        }
        else {
            navigateTo("/parliament/candidates")
        }
    }

    let openModal


    // --- pagination and search ---
    let currentPage = 1;
    let filter = ""
    const perPage = 5;
    let filtered = []  // filtered parties
    let paginated = []  // = filtered and paginated parties

    // update filtered and paginated on change
    $: filtered = filterCandidate($config.parties, filter)
    $: paginated = paginate(filtered, currentPage, perPage)
</script>

<style lang="scss">
  .nextBtn {
    display: flex;
    justify-content: flex-end;
  }

  .parties {
    display: flex;
    gap: 5px;
    flex-direction: column;
    margin-bottom: 2rem;
  }
</style>


<MainLayout>
    <span slot="subtitle">{$config.subtitle}</span>
    <Search title="Kandidujúce strany:" bind:filter placeholder="Vyhľadajte stranu"/>
    <i>Kliknutím označte stranu, ktorú chcete voliť.</i>

    <div class="parties">
        {#each paginated as party}
            <PartyBox party={party} isSelected={party.id === $chosenParty?.id} showCheckbox={true} on:click="{() => chooseParty(party)}"/>
        {/each}
    </div>

    <Pagination itemsCount={filtered.length} itemsPerPage={perPage} bind:currentPage/>

    <div class="nextBtn">
        <PrimaryButton text="Potvrdiť" on:click={openModal}/>
    </div>
    {#if $chosenParty !== null}
        <Modal bind:openModal yesCallback={()=>chooseCandidates()} yesTxt="Potvrdiť" cancelTxt="Upraviť">
            <span slot="title">Zvolili ste</span>
            <PartyBox party={$chosenParty} />
        </Modal>
    {:else}
        <Modal bind:openModal yesCallback={()=>chooseCandidates()} yesTxt="Odoslať prázdny hlas" cancelTxt="Upraviť">
            <span slot="title">Nezvolili ste žiadnu stranu</span>
            <span slot="subtitle">Naozaj chcete odoslať prázdny hlas?</span>
        </Modal>
    {/if}
</MainLayout>