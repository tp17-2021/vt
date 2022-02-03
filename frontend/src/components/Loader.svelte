<script lang="ts">
    type tIcon = 'spinner' | 'token'
    export let icon: tIcon = "spinner"
    export let title = ""
</script>


<style lang="scss">
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

      i {
        font-size: clamp(12px, 60vw, 256px);
        margin-bottom: 3rem;
      }

      i.rotate {
        animation: rotate 2s linear infinite;
      }

      @keyframes rotate {
        from {
          transform: rotate(0deg);
        }
        to {
          transform: rotate(360deg);
        }
      }

      h1 {
        padding-top: 2rem;
      }
    }
  }

  .fas {
    color: var(--blue);
  }

  .fa-check {
    color: var(--green);
  }

  .fa-times {
    color: var(--red);
  }
</style>

<div class="centered">
    <div>
        {#if icon === 'spinner'}
            <i class="fas fa-spinner rotate"></i>
        {:else if icon === 'success'}
            <i class="fas fa-check"></i>
        {:else if icon === 'error'}
            <i class="fas fa-times"></i>
        {:else if icon === 'token'}
            <img src="/img/insert-token.png" alt="">
        {/if}

        <h1>{title}</h1>
        <slot></slot>
    </div>
</div>
