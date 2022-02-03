<script lang="ts">
    import MainLayout from "../../parts/layouts/MainLayout.svelte";
    import {config, chosenCandidates, chosenParty} from "../../stores";
    import PrimaryButton from "../../components/buttons/PrimaryButton.svelte";
    import Modal from "../../components/Modal.svelte";
    import {navigateTo} from "svelte-router-spa";
    import Pagination from "../../components/Pagination.svelte";
    import {paginate} from "../../helpers/pagination";
    import {filterCandidate} from "../../helpers/filter";
    import Search from "../../components/Search.svelte";
    import Warning from "../../components/Warning.svelte";
    import CandidateBox from "./components/CandidateBox.svelte";
    import BackButton from "../../components/buttons/BackButton.svelte";

    let maxCandidates = 5;  // max candidates to be chosen


    // --- pagination and search ---
    let currentPage = 1;
    let filter = ""
    const perPage = 10;
    let filtered = []  // filtered candidates
    let paginated = []  // = filtered and paginated candidates

    // update filtered and paginated on change
    $: filtered = $chosenParty ? filterCandidate($chosenParty.candidates, filter) : [];
    $: paginated = paginate(filtered, currentPage, perPage)

    // --- set and remove chosen candidates ---
    // if candidate is already chosen, remove it from the list
    // else add it to the list
    function chooseCandidate(candidate) {


        if ($chosenCandidates.includes(candidate)) {
            console.log("chooseCandidate remove", candidate.name)
            $chosenCandidates = [...$chosenCandidates.filter(c => c !== candidate)];

        } else if ($chosenCandidates.length < maxCandidates) {
            console.log("chooseCandidate add", candidate.name)
            $chosenCandidates = [...$chosenCandidates, candidate];

            if ($chosenCandidates.length === maxCandidates) {
                openConfirmModal()
            }
        } else {
            openErrorModal()
        }

    }

    // --- confirm vote ---
    let openErrorModal;
    let openConfirmModal;

    function sendVote() {
        console.log("TODO: sendVote");
        navigateTo('/parliament/confirm');
    }
</script>

<style lang="scss">
  .buttonArea {
    display: flex;
    justify-content: end;
    width: 100%;
  }

  .chosenCandidates {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    width: 100%;
    min-height: 50px;


    .chosenCandidate {
      display: flex;
      padding: 0 2rem 0 0;
      gap: 5px;
      font-weight: bold;

      .name {
        color: #003078;
      }

      .xButton {
        color: #E54957;
        border: none;
        background: none;

        font-size: 2rem;
        margin-top: -15px;
      }
    }
  }

  .candidateCount {
    font-weight: bold;
    color: green;
  }

  .candidates {
    display: grid;
    padding-bottom: 2rem;

    .legend {
      display: grid;
      grid-template-columns: 20fr 5fr 7fr 10fr 7fr;
      gap: 10px;
      font-weight: bold;
      padding: 0 2rem;
    }
  }


  .modalCandidates {
    font-weight: bold;
    margin-bottom: 1rem;
  }

</style>

<MainLayout>
    <span slot="subtitle">{$chosenParty?.name}</span>
    <div class="chosenCandidates">
        {#each $chosenCandidates as candidate}
            <div class="chosenCandidate">
                <div class="name">{candidate.name}</div>
                <div class="xButton" on:click={()=>chooseCandidate(candidate)}>&times;</div>
            </div>
        {/each}
        {#if $chosenCandidates.length === maxCandidates}
            <div class="candidateCount">Zvolili ste maximálny počet kandidátov</div>
        {:else}
            <div class="candidateCount">Ešte môžete zvoliť {maxCandidates - $chosenCandidates.length} kandidátov</div>
        {/if}
    </div>

    <Search title="Kandidáti:" bind:filter placeholder="Vyhľadajte kandidáta"/>
    <i>Kliknutím označte 5 poslancov, ktorých chcete voliť.</i>

    <div class="candidates">
        <div class="legend">
            <span>Meno</span>
            <span>Tituly</span>
            <span>Vek</span>
            <span>Povolanie</span>
            <span>Bydlisko</span>
        </div>
        {#each paginated as candidate, index}
            <CandidateBox showCheckbox={true} candidate={candidate} isSelected={$chosenCandidates.indexOf(candidate) > -1} on:click={()=>chooseCandidate(candidate)}/>
        {/each}

        <Pagination itemsCount={filtered.length} itemsPerPage={perPage} bind:currentPage/>
    </div>


    <div class="buttonArea">
        <BackButton />
        <PrimaryButton on:click={()=>openConfirmModal()}>
            Potvrdiť <i class="fas fa-chevron-right"></i>
        </PrimaryButton>
    </div>

    <Modal bind:openModal={openErrorModal} yesTxt="Odoslať hlas" cancelTxt="Späť">
        <span slot="title">Už ste si zvolili 5 kandidátov</span>
        <span slot="subtitle">Je možné zvoliť iba maximálne {maxCandidates} kandidátov</span>
    </Modal>
    <Modal bind:openModal={openConfirmModal} yesCallback={()=>sendVote()} yesTxt="Pokračovať" cancelTxt="Upraviť">
        <span slot="title">Zvolili ste</span>
        {#if $chosenCandidates.length === 0}
            <h1>žiadneho kandidáta, potvrdiť odoslanie prázdneho hlasu?</h1>
        {:else}
            <div class="modalCandidates">
                {#each $chosenCandidates as candidate}
                    <div>
                        <div class="name">{candidate.id}. {candidate.name}</div>
                    </div>
                {/each}
            </div>
            {#if $chosenCandidates.length < maxCandidates}
                <Warning text={"Ešte môžete zvoliť ďalších " + (maxCandidates - $chosenCandidates.length) + " kandidátov"}/>
            {/if}
            <p>Ak chcete upraviť svoju voľbu, stlačte tlačidlo upraviť</p>
        {/if}

    </Modal>
</MainLayout>