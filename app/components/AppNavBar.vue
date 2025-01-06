<template>
  <div class="navbar bg-base-100 relative">
    <div class="mx-auto w-full max-w-[2560px] px-4 sm:px-8 2xl:px-16 flex items-center justify-between">

      <div class="flex">
        <a class="btn btn-neutral text-xl">LOGO</a>
      </div>

      <label class="input bg-neutral input-ghost flex items-center gap-2 max-w-[480px] w-full">
        <input type="text" class="grow" placeholder="Search" />
        <Icon icon="solar:magnifer-linear" width="24" height="24" />

      </label>

      <div class="flex-none">
        <button class="btn btn-neutral text-xl mr-4">
          <Icon icon="solar:wallet-2-bold" :ssr="true" class="text-2xl" />
          Login
        </button>
        <button class="btn btn-neutral btn-square">
          <Icon icon="solar:cart-large-bold" class="text-2xl" />
        </button>
      </div>

    </div>
  </div>
</template>

<style scoped>
.navbar {
  /*border-bottom: 1px solid #212121;*/
}

.searchbar-container {
  max-width: 480px;
  height: 48px;
  padding: 4px;
}
</style>
