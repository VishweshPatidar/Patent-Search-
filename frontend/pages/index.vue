<template>
	<div class="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100">
		<!-- Enhanced Header Section with Glassmorphism -->
		<div class="bg-white/60 backdrop-blur-md border-b border-white/20 sticky top-0 z-10 shadow-sm">
			<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
				<div class="flex items-center justify-between">
					<div class="flex items-center space-x-4">
						<div class="w-12 h-12 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-xl flex items-center justify-center shadow-lg hover:shadow-xl hover:scale-105 transition-all duration-300 cursor-pointer">
							<svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
							</svg>
						</div>
						<div>
							<h1 class="text-3xl font-bold bg-gradient-to-r from-gray-900 via-blue-800 to-indigo-800 bg-clip-text text-transparent">
								Patent Search
							</h1>
							<p class="text-sm text-gray-600 font-medium">Advanced Technical Document Discovery</p>
						</div>
					</div>
					<div class="hidden sm:flex items-center space-x-2 text-sm text-gray-600 bg-white/50 px-3 py-2 rounded-full">
						<svg class="w-4 h-4 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
						</svg>
						<span class="font-medium">{{ results.length }} results found</span>
					</div>
				</div>
			</div>
		</div>

		<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
			<!-- Enhanced Search Section -->
			<div class="bg-white/60 backdrop-blur-md rounded-3xl shadow-2xl border border-white/30 p-8 sm:p-12 mb-12">
				<div class="max-w-5xl mx-auto">
					<div class="text-center mb-10">
						<h2 class="text-4xl sm:text-5xl font-bold text-gray-900 mb-4 bg-gradient-to-r from-gray-900 to-blue-800 bg-clip-text text-transparent">
							Discover Innovation
						</h2>
						<p class="text-lg text-gray-600 max-w-2xl mx-auto">Search through thousands of patents and research papers with AI-powered semantic search</p>
					</div>
					
					<div class="relative">
						<!-- Google-style Search Bar -->
						<div class="flex items-center bg-white rounded-2xl shadow-xl border-2 border-gray-200/50 hover:border-blue-300/50 focus-within:border-blue-400/50 focus-within:shadow-2xl transition-all duration-300 overflow-hidden">
							<div class="flex-1 relative">
								<input 
									v-model="query" 
									@keyup.enter="onSearch" 
									type="text" 
									placeholder="Search for patents, technologies, or research topics..." 
									class="w-full px-8 py-6 text-lg border-0 focus:ring-0 focus:outline-none placeholder-gray-400 bg-transparent"
								/>
								<div class="absolute right-6 top-1/2 transform -translate-y-1/2">
									<svg class="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
										<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
									</svg>
								</div>
							</div>
							<!-- Enhanced Search Button -->
							<button 
								@click="onSearch" 
								:disabled="loading"
								class="bg-gradient-to-r from-blue-600 to-indigo-600 text-white px-10 py-6 font-semibold hover:from-blue-700 hover:to-indigo-700 hover:shadow-xl hover:-translate-y-0.5 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:translate-y-0 flex items-center space-x-3 rounded-r-2xl"
							>
								<!-- Enhanced Loading Animation -->
								<div v-if="loading" class="flex items-center space-x-2">
									<div class="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
									<span>Searching</span>
								</div>
								<div v-else class="flex items-center space-x-2">
									<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
										<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
									</svg>
									<span>Search</span>
								</div>
							</button>
						</div>
						<p v-if="error" class="text-red-600 mt-4 text-center font-medium">{{ error }}</p>
					</div>
				</div>
			</div>

			<!-- Enhanced Loading State -->
			<div v-if="loading" class="flex items-center justify-center py-16">
				<div class="text-center">
					<div class="w-16 h-16 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin mx-auto mb-6"></div>
					<p class="text-gray-600 text-lg font-medium">Searching through our database...</p>
				</div>
			</div>

			<!-- Results Section -->
			<ResultsList v-if="results.length" :results="results" />

			<!-- Enhanced Analytics Dashboard -->
			<div v-if="results.length" class="mt-16 grid grid-cols-1 lg:grid-cols-2 gap-8">
				<!-- Topic Clusters Card -->
				<div class="bg-gradient-to-br from-purple-50 to-pink-50 backdrop-blur-sm rounded-3xl shadow-xl border border-purple-200/30 p-8 hover:shadow-2xl hover:scale-[1.02] transition-all duration-300">
					<div class="flex items-center mb-6">
						<div class="w-14 h-14 bg-gradient-to-r from-purple-500 to-pink-500 rounded-2xl flex items-center justify-center mr-4 shadow-lg animate-pulse">
							<svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path>
							</svg>
						</div>
						<div>
							<h3 class="text-2xl font-bold text-gray-900">Topic Clusters</h3>
							<p class="text-gray-600">AI-powered analysis</p>
						</div>
					</div>
					<p class="text-gray-600 mb-6 text-lg">Intelligent topic clustering coming soon</p>
					<div class="space-y-3">
						<div class="flex items-center justify-between p-4 bg-white/70 rounded-xl hover:bg-white/90 transition-colors duration-200">
							<span class="text-sm font-semibold text-gray-800">Machine Learning</span>
							<span class="text-xs text-gray-600 bg-purple-100 px-3 py-1 rounded-full">12 patents</span>
						</div>
						<div class="flex items-center justify-between p-4 bg-white/70 rounded-xl hover:bg-white/90 transition-colors duration-200">
							<span class="text-sm font-semibold text-gray-800">Blockchain</span>
							<span class="text-xs text-gray-600 bg-purple-100 px-3 py-1 rounded-full">8 patents</span>
						</div>
					</div>
				</div>
				
				<!-- Trend Analysis Card -->
				<div class="bg-gradient-to-br from-green-50 to-teal-50 backdrop-blur-sm rounded-3xl shadow-xl border border-green-200/30 p-8 hover:shadow-2xl hover:scale-[1.02] transition-all duration-300">
					<div class="flex items-center mb-6">
						<div class="w-14 h-14 bg-gradient-to-r from-green-500 to-teal-500 rounded-2xl flex items-center justify-center mr-4 shadow-lg animate-pulse">
							<svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
							</svg>
						</div>
						<div>
							<h3 class="text-2xl font-bold text-gray-900">Trend Analysis</h3>
							<p class="text-gray-600">Publication insights</p>
						</div>
					</div>
					<p class="text-gray-600 mb-6 text-lg">Publication trends over time</p>
					<div class="bg-white/70 rounded-2xl p-4 shadow-inner">
						<canvas ref="trendCanvas" height="200" class="w-full rounded-xl"></canvas>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
import ResultsList from '~/components/ResultsList.vue'

const query = ref('')
const results = ref<any[]>([])
const loading = ref(false)
const error = ref('')
const trendCanvas = ref<HTMLCanvasElement | null>(null)
let chart: any = null

const BACKEND_URL = (process.env.NUXT_PUBLIC_BACKEND_URL || 'http://localhost:8000').replace(/\/$/, '')

async function onSearch() {
	if (!query.value.trim()) {
		error.value = 'Please enter a query.'
		return
	}
	error.value = ''
	loading.value = true
	try {
		const resp = await fetch(`${BACKEND_URL}/search?query=` + encodeURIComponent(query.value))
		const data = await resp.json()
		results.value = data.results || []
		updateTrend()
	} catch (e: any) {
		error.value = e?.message || 'Failed to fetch results.'
	} finally {
		loading.value = false
	}
}

function updateTrend() {
	// Simple trend visualization without Chart.js for now
	const yearToCount: Record<string, number> = {}
	for (const r of results.value) {
		const y = r.year ?? 'Unknown'
		yearToCount[y] = (yearToCount[y] || 0) + 1
	}
	console.log('Trend data:', yearToCount)
}

watch(results, updateTrend)
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>


