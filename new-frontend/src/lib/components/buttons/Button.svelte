<script lang="ts">
    export let href = "";
    export let type = "secondary";

    /**
     * https://idsk.gov.sk/komponenty/tlacidla
     * Text made bigger
     * removed bottom margin
     */
</script>

<style lang="scss">
  button {
    text-size-adjust: 100%;
    font-family: "Source Sans Pro", "Arial", sans-serif;
    -webkit-font-smoothing: antialiased;
    font-weight: 400;
    font-size: 1rem;
    line-height: 1.1875;
    box-sizing: border-box;
    display: inline-block;
    position: relative;
    width: 100%;
    margin-top: 0;
    border: 2px solid transparent;
    border-radius: 0;
    text-align: center;
    vertical-align: top;
    cursor: pointer;
    -webkit-appearance: none;
    background-color: #f3f2f1;
    box-shadow: 0 2px 0 #929191;
    color: #0b0c0c;

    //padding: 8px 10px 7px;
    padding: 15px 10px;
    margin-bottom: .5rem;

    //display: grid;
    //place-items: center;
    //background-color: #cecece;
    //padding: 20px;
    //border-bottom: 5px solid black;
    //width: 100%;
  }

  .secondary {

  }

  .primary {
    background-color: var(--green);
    color: white;
    box-shadow: 0 2px 0 #002d18;
  }

  a {
    text-decoration: none;
  }
</style>

{#if href !== ""}
    <a {href}>
        <button on:click class={type === "secondary" ? "secondary" : "primary"}>
            <slot></slot>
        </button>
    </a>
{:else}
    <button on:click class={type === "secondary" ? "secondary" : "primary"}>
        <slot></slot>
    </button>
{/if}