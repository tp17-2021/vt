<script lang="ts">
    import Header from "../lib/components/header/Header.svelte";
    import BreadCrumb from "../lib/components/header/BreadCrumb.svelte";
    import Spinner from "../lib/components/spinner/Spinner.svelte";
    import { goto } from "@roxi/routify";
    import { onMount } from "svelte";
    import { ElectionStatus, electionStatus } from "../api/websocket";
    import {configLoaded, electionType} from "../api/stores";

    function statusChanged(electionStatus, configLoaded): void {
        if (configLoaded) {
            console.log("Voting status changed:", electionStatus);
            if (electionStatus === ElectionStatus.ELECTIONS_NOT_STARTED) {
                $goto(`/disabled`);
            } else if (electionStatus === ElectionStatus.TOKEN_VALID) {
                $goto(`/${$electionType}/party`);
            } else if (electionStatus === ElectionStatus.TOKEN_NOT_VALID) {
                $goto("/error");
            } else if (electionStatus === ElectionStatus.WAITING_FOR_NFC_TAG) {
                $goto("/enabled");
            } else {
                alert("Unknown voting status: " + electionStatus);
            }
        } else {
            console.log("Config not loaded yet, waiting for it...");
        }
    }

    $: statusChanged($electionStatus, $configLoaded);
    onMount(() => {
        statusChanged($electionStatus, $configLoaded);
    });
</script>

{#if $configLoaded}
    <Header />
    <main>
        <BreadCrumb />
        <Spinner />
        <slot />
    </main>
{:else}
    <p>Loading config...</p>
{/if}

<style>
    main,
    .full-modal {
        flex: 1;
        display: flex;
        flex-direction: column;
        padding: 1rem;
        width: 100%;
        max-width: 768px;
        margin: 0 auto;
        box-sizing: border-box;
    }
</style>
