<template>
    <div class="wrapper">
        <div class="title">
            <h1>物價趨勢</h1>
        </div>
        
        <div class="content">
            <div class="selects">

                <select v-model="selectedCategory">
                    <option disabled value="">請選擇商品類別</option>
                    <option v-for="category in categoryKeys" :key="category" :value="category">{{
                        categoryName(category)}}</option>
                </select>
                <select v-model="selectedProduct" style="margin-top: 5px;">
                    <option disabled value="">請選擇商品</option>
                    <option v-for="product in products" :key="product.產品名稱" :value="product">{{ product.產品名稱 }}</option>
                </select>
            </div>
            <div v-if="selectedProduct" class="visualize">
                <TrendingChart v-if="selectedProduct" :data="selectedProduct"></TrendingChart>
                <TrendingTable v-if="selectedProduct" :data="selectedProduct" class="trendtable"></TrendingTable>
            </div>
        </div>
    </div>
</template>

<script>
import { usePricesStore } from '@/stores/prices';
import Categories from '@/constants/categories';
import TrendingTable from '@/components/TrendingTable.vue';
import TrendingChart from '@/components/TrendingChart.vue';

export default {
    components: {
        TrendingTable,
        TrendingChart
    },
    data() {
        return {
            selectedCategory: '',
            selectedProduct: '',
            productList: [],
        };
    },
    computed: {
        store() {
            return usePricesStore();
        },
        categoryKeys() {
            return Object.keys(Categories);
        },
        products() {
            return this.selectedCategory ? this.store.getPricesByCategory(this.selectedCategory) : [];
        },
    },
    methods: {
        categoryName(category) {
            return Categories[category];
        }
    },
    watch: {
        selectedCategory() {
            this.selectedProduct = '';
            const store = usePricesStore();
            this.productList = store.getProductList(this.selectedCategory);
            this.productData = null;
        },
        selectedProduct() {
            console.log(this.selectedProduct);
        }
    },
    created() {
        const store = usePricesStore();
        store.fetchPrices();
    }
};
</script>


<style scoped>
.wrapper {
    padding: 3em 5em;
    background: #f3f3f3;
    min-height: calc(100vh - 4.5em);
    height: calc(100% - 4.5em);
    box-sizing: border-box;
    /*max-width: 100vw;*/
}

.content {
    margin-top: 2em;
    background-color: #fff;
    border-radius: 1em;
    padding: 2em;
    /*max-width: 100vw;*/
}


.selects {
    display: flex;
    justify-content: flex-start;
    flex-wrap: wrap;
    /*max-width: 100vw;*/
}

.selects>select {
    padding: .5em;
    font-size: 1.1em;
    margin-right: 1em;
    margin-bottom: 2px;
    border-radius: .5em;
    border: 1px solid #ccc;
    outline: none;
    cursor: pointer;
    appearance: auto !important;
}

.visualize > * {
    flex: 1 1 50%;
    box-sizing: border-box;
    padding: 1em;
}
@media (max-width: 768px) {
    .wrapper{
        padding: 3em 1em 0em 1em;
    }
    .content {
        padding-top: 2em;
        
        /*max-width: 100vw;*/
    }
    .title{
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
    }
    .trendtable{
        overflow-x: auto;
    }
    /*.visualize  {
        display: flex;
        justify-content: flex-start;
        flex-wrap: wrap;
    }*/
}
</style>