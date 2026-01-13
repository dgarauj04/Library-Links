<script setup>
  defineProps({
    show: {
      type: Boolean,
      default: false
    },
    type: {
      type: String,
      default: 'error', 
      validator: (value) => ['error', 'success'].includes(value)
    },
    message: {
      type: String,
      required: true
    }
  })

  defineEmits(['dismiss'])
</script>

<template>
  <div
    v-if="show"
    :class="[
      'rounded-md p-4 text-sm',
      type === 'error' ? 'bg-red-100 text-red-700 dark:bg-red-900/[.3] dark:text-red-300' : '',
      type === 'success' ? 'bg-green-100 text-green-700 dark:bg-green-900/[.3] dark:text-green-300' : ''
    ]"
    role="alert"
  >
    <div class="flex">
      <div class="flex-shrink-0">
        <svg v-if="type === 'error'" class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
          <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.28 7.22a.75.75 0 00-1.06 1.06L8.94 10l-1.72 1.72a.75.75 0 101.06 1.06L10 11.06l1.72 1.72a.75.75 0 101.06-1.06L11.06 10l1.72-1.72a.75.75 0 00-1.06-1.06L10 8.94 8.28 7.22z" clip-rule="evenodd" />
        </svg>
        <svg v-if="type === 'success'" class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
          <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.857-9.809a.75.75 0 00-1.214-.882l-3.483 4.79-1.88-1.88a.75.75 0 10-1.06 1.061l2.5 2.5a.75.75 0 001.137-.089l4-5.5z" clip-rule="evenodd" />
        </svg>
      </div>
      <div class="ml-3">
        <p>{{ message }}</p>
      </div>
      <div class="ml-auto pl-3">
        <div class="-mx-1.5 -my-1.5">
          <button
            @click="$emit('dismiss')"
            :class="[
              'inline-flex rounded-md p-1.5 focus:outline-none focus:ring-2 focus:ring-offset-2',
              type === 'error' ? 'hover:bg-red-200 dark:hover:bg-red-900/50 focus:ring-red-600 focus:ring-offset-red-100' : '',
              type === 'success' ? 'hover:bg-green-200 dark:hover:bg-green-900/50 focus:ring-green-600 focus:ring-offset-green-100' : ''
            ]"
          >
            <span class="sr-only">Dismiss</span>
            <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
              <path d="M6.28 5.22a.75.75 0 00-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 101.06 1.06L10 11.06l3.72 3.72a.75.75 0 101.06-1.06L11.06 10l3.72-3.72a.75.75 0 00-1.06-1.06L10 8.94 6.28 5.22z" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>