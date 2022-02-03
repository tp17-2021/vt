<script lang="ts">
    import MainLayout from "../parts/layouts/MainLayout.svelte";
</script>


<style type="text/scss">
  .centered {
    display: grid;
    place-items: center;
    width: 100%;
    height: 80vh;

    > div {
      display: flex;
      flex-direction: column;
      align-items: center;
      text-align: center;
    }
    object {
      width: 50vw;
      height: 50vw;
      margin-bottom: 4rem;
    }
  }
</style>

<MainLayout>
    <div class="centered">
        <div>
            <object data="/img/insert_token.svg" type="image/svg+xml" class="mylogo"></object>
            <h1>Vložte prosím autorizačný token do čítačky</h1>
        </div>
    </div>
</MainLayout>