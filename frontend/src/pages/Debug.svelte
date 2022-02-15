<script lang="ts">
    import {chosenParty, config, debugEnabled, tokenValid} from "../stores";
    import {get} from "svelte/store";



    if ($debugEnabled) {
        console.warn('Debug mode enabled, because localhost:5000 is used');

        tokenValid.set(true);
        chosenParty.set(get(config).parties[0]);
    }
    else
    {
        console.warn('Debug mode disabled, because localhost:5000 is not used');
    }

</script>


{#if $debugEnabled}
    <div>
        <div>
            <label>
                <input type=checkbox bind:checked={$tokenValid}>
                Token valid
            </label>
        </div>
    </div>
{/if}
