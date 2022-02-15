<script lang="ts">
    import MainLayout from "../../parts/layouts/MainLayout.svelte";
    import {chosenCandidates, chosenParty} from "../../stores";
    import PrimaryButton from "../../components/buttons/PrimaryButton.svelte";
    import {navigateTo} from "svelte-router-spa";
    import Warning from "../../components/Warning.svelte";
    import Party from "./components/PartyBox.svelte";
    import CandidateBox from "./components/CandidateBox.svelte";
    import BackButton from "../../components/buttons/BackButton.svelte";

    function confirmVote() {
        navigateTo('/parliament/send')
    }
</script>

<style lang="scss">
</style>

<MainLayout>
    <span slot="title">POTVRDENIE VOĽBY</span>

    <h2>Zvolená strana</h2>
    {#if $chosenParty === null}
        <Warning text="Nezvolili ste žiadnu politickú stranu" />
    {:else}
        <Party party={$chosenParty}/>
    {/if}

    <h2 class="mt-3">Zvolení kandidáti na poslancov</h2>
    <div class="chosen-candidates">
        {#if $chosenCandidates.length === 0}
            <Warning text="Nezvolili ste žiadneho kandidáta" />
        {/if}
        {#each $chosenCandidates as candidate}
            <CandidateBox candidate={candidate}/>
        {/each}
    </div>

    <div class="buttonArea">
        <BackButton />
        <PrimaryButton on:click={()=>confirmVote()}>
            Odoslať hlas
        </PrimaryButton>
    </div>

</MainLayout>