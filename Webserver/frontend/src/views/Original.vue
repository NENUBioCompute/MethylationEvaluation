<template>
  <div class="originalBox">
    <b-row>
      <h3>The Original Age Prediction Method Based on <i>Deep Learning</i></h3>
    </b-row>
    <hr />
    <b-row>
      <h3><a style="color:red">PerSEClock </a>(reference link)</h3>
    </b-row>
    <b-row>
      <h4>1. Introduction</h4>
      <p>
        A perceptron model based on the attention mechanism, and use Illumina DNA methylation array datasets from
        35 different tissues for model training and testing. The feature selection of the method upholds the principle of
        comprehensive criteria, and the model is constructed using a total of 24516 CpG sites in 27K, 450K and 850K.
      </p>
    </b-row>
    <b-row>
      <h4>2. The network structure of the model</h4>
      <p>The model which consists of two parts: the channel attention module and the perceptron module. Since the
        combination of CpG loci used in the elastic net is screened using the feature selection method, the impact of the
        deleted CpG loci on age prediction is not considered. Therefore, this paper does not use any filtered CpG method
        and proposes to use a channel attention mechanism to assign different weights to feature values so that the model
        focuses on task-relevant CPG features and reduces the weights of irrelevant CpG features to provide more valid
        information for high-level prediction tasks. The perceptron module is connected after the channel attention
        module, and the weighted data are fed into a 4-layer network for fitting, and the final regression output predicts
        age.</p>
      <img style="width: 75%; margin: 0 auto;" src="../assets/model/model_PerMLP.png" />
      <i style="width: 75%; margin: 0 auto; text-align: center;">Fig 1 Model architecture</i>
    </b-row>
    <b-row>
      <h4>3. Train And Test</h4>
    </b-row>
    <b-row>
      <img style="width: 60%; margin: 0 auto;" src="../assets/model/alldata_permlp.png" />
      <i style="width: 60%; margin: 0 auto; text-align: center;">Fig 2 all data</i>
    </b-row>
    <b-row>
      <img style="width: 30%; margin: 0 auto;" src="../assets/model/train_permlp.png" />
      <img style="width: 30%; margin: 0 auto;" src="../assets/model/test_permlp.png" />
      <img style="width: 30%; margin: 0 auto;" src="../assets/model/val_permlp.png" />
      <i style="width: 30%; margin: 0 auto; text-align: center;">Fig 3 train data</i>
      <i style="width: 30%; margin: 0 auto; text-align: center;">Fig 4 test data</i>
      <i style="width: 30%; margin: 0 auto; text-align: center;">Fig 5 val data</i>
    </b-row>
    <b-row>
      <h4>4. Result</h4>
    </b-row>
  </div>
</template>

<script>
export default {
  data () {
    return {
    }
  },

  methods: {}
}

</script>
<style scoped>.originalBox {
  margin: auto;
  margin-top: 20px;
  width: 80%;
}</style>
