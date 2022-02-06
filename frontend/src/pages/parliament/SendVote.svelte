<script lang="ts">
    import MainLayout from "../../parts/layouts/MainLayout.svelte";
    import Loader from "../../components/Loader.svelte";
    import {Navigate, navigateTo} from "svelte-router-spa";
    import {chosenCandidates, chosenParty, resetVote, resetVoteStores} from "../../stores";
    import axios from "axios";
    import {sendVoteParliament} from "../../api/rest";
    import PrimaryButton from "../../components/buttons/PrimaryButton.svelte";

    let printing = true;
    let success = false;

    // wait for printer
    (async () => {
        let partyNumber = $chosenParty?.party_number
        let candidates = $chosenCandidates.map(candidate => candidate.id)
        console.log("sendVoteParliament", partyNumber, candidates);
        let res = await sendVoteParliament(partyNumber, candidates);
        console.log("sendVoteParliament res", res);
        printing = false;

        if (res !== null) {
            success = true;
            setTimeout(resetVote, 5000);
        } else {
            success = false;
            alert("vyskytla sa chyba");
        }
    })();

</script>

<MainLayout>
    {#if printing}
        <Loader icon="spinner" title="VÁŠ HLAS BOL ZAPOČÍTANÝ">
            <div>Čakajte prosím</div>
            <div>Prebieha tlač hlasovacieho lístka</div>
        </Loader>
    {:else if success}
        <Loader icon="success" title="VÁŠ HLAS BOL ZAPOČÍTANÝ">
            <div>Ďakujeme za vašu účasť</div>
        </Loader>
    {:else}
        <Loader icon="error" title="VÁŠ HLAS NEBOL ZAPOČÍTANÝ">
            <div class="pb-3">Nastala chyba, <b>prosím zavolajte obsluhu</b></div>
            <PrimaryButton on:click={()=>resetVote()}>
                <i class="fas fa-home"></i> Späť domov
            </PrimaryButton>
        </Loader>
    {/if}
</MainLayout>