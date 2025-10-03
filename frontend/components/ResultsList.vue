<template>
	<div class="space-y-8">
		<!-- Enhanced Results Header -->
		<div class="flex items-center justify-between mb-8">
			<div>
				<h2 class="text-3xl font-bold text-gray-900 mb-2">Search Results</h2>
				<p class="text-gray-600">Discover relevant patents and research papers</p>
			</div>
			<div class="flex items-center space-x-3 bg-white/60 backdrop-blur-sm px-4 py-3 rounded-full shadow-lg border border-white/30">
				<svg class="w-5 h-5 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
				</svg>
				<span class="font-semibold text-gray-700">{{ results.length }} documents found</span>
			</div>
		</div>

		<!-- Enhanced Results Grid -->
		<div class="grid gap-8">
			<div 
				v-for="(r, idx) in results" 
				:key="idx" 
				class="group bg-white/70 backdrop-blur-sm rounded-3xl shadow-xl border border-white/40 hover:shadow-2xl hover:scale-[1.02] hover:border-blue-200/50 transition-all duration-300 overflow-hidden"
			>
				<div class="p-8">
					<!-- Enhanced Header with title and score -->
					<div class="flex items-start justify-between mb-6">
						<div class="flex-1">
							<div class="flex items-center space-x-4 mb-3">
								<div class="w-12 h-12 bg-gradient-to-r from-blue-500 to-indigo-500 rounded-2xl flex items-center justify-center shadow-lg group-hover:shadow-xl transition-shadow duration-300">
									<svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
										<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
									</svg>
								</div>
								<div class="flex-1">
									<h3 class="text-xl font-bold text-gray-900 group-hover:text-blue-600 transition-colors duration-300 line-clamp-2 leading-tight">
										{{ r.title }}
									</h3>
								</div>
							</div>
						</div>
						<!-- Enhanced Relevance Score Badge -->
						<div class="ml-6">
							<div class="bg-gradient-to-r from-green-400 to-blue-500 text-white px-4 py-2 rounded-full shadow-lg">
								<div class="text-center">
									<div class="text-lg font-bold">{{ Math.round(r.score * 100) }}%</div>
									<div class="text-xs opacity-90">Relevance</div>
								</div>
							</div>
						</div>
					</div>

					<!-- Enhanced Abstract -->
					<div class="mb-6">
						<p class="text-gray-700 leading-relaxed line-clamp-3 text-lg">
							{{ r.abstract }}
						</p>
					</div>

					<!-- Enhanced Footer with metadata -->
					<div class="flex items-center justify-between pt-6 border-t border-gray-200/50">
						<div class="flex items-center space-x-6">
							<div class="flex items-center space-x-2 text-sm text-gray-600 bg-gray-50 px-3 py-2 rounded-full">
								<svg class="w-4 h-4 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
									<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
								</svg>
								<span class="font-semibold">{{ r.year ?? 'N/A' }}</span>
							</div>
							<div class="flex items-center space-x-2 text-sm text-gray-600 bg-gray-50 px-3 py-2 rounded-full">
								<svg class="w-4 h-4 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
									<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"></path>
								</svg>
								<span class="font-semibold">{{ r.id }}</span>
							</div>
						</div>
						<div class="flex items-center space-x-3">
							<button class="px-6 py-3 text-sm font-semibold text-blue-600 hover:text-blue-700 hover:bg-blue-50 rounded-xl transition-all duration-200 hover:shadow-md">
								View Details
							</button>
							<button class="p-3 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-xl transition-all duration-200 hover:shadow-md">
								<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
									<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z"></path>
								</svg>
							</button>
						</div>
					</div>
				</div>
			</div>
		</div>

		<!-- Enhanced Load More Button -->
		<div v-if="results.length >= 20" class="text-center pt-8">
			<button class="px-12 py-4 bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-bold rounded-2xl hover:from-blue-700 hover:to-indigo-700 hover:shadow-2xl hover:-translate-y-1 transition-all duration-300 shadow-xl">
				Load More Results
			</button>
		</div>
	</div>
</template>

<script setup lang="ts">
import { defineProps } from 'vue'

defineProps<{ results: Array<any> }>()
</script>


