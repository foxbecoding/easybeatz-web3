<template>
  <div class="drawer lg:drawer-open">
    <input id="my-drawer-2" type="checkbox" class="drawer-toggle" />
    <div class="drawer-content flex flex-col ">

      <AppNavBar />
      <div class="divider my-0" style="height: 0rem"></div>
      <main>
        <slot />
      </main>

    </div>
    <div class="drawer-side">
      <label for="my-drawer-2" aria-label="close sidebar" class="drawer-overlay"></label>
      <ul class="menu bg-base-200 text-base-content min-h-full w-80 px-4 py-2">
        <!-- Sidebar content here -->
        <img src="/logo.png" width="150px" class="px-4 pb-8" />
        <li>
          <a class="text-lg">
            <Icon icon="solar:home-2-bold" width="24" height="24" />
            Home
          </a>
        </li>
        <li>
          <a class="text-lg">
            <Icon icon="solar:turntable-music-note-bold" width="24" height="24" />
            Explore
          </a>
        </li>
        <li>
          <a class="text-lg">
            <Icon icon="solar:music-library-2-bold" width="24" height="24" />
            Library
          </a>
        </li>
        <li>
          <a class="text-lg">
            <Icon icon="solar:upload-track-2-bold" width="24" height="24" />
            Upload
          </a>
        </li>
        <li>
          <a class="text-lg">
            <Icon icon="solar:playlist-2-bold" width="24" height="24" />
            Playlist
          </a>
        </li>
      </ul>
    </div>
  </div>
</template>
