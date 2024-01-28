library(data.table)
library(ggplot2) 
library(moments)

sink("statistics_output.txt")

#--------------------------------------------
#Descriptive statistics on whole data (Fairness)
#--------------------------------------------

datacomplete <- data.table::fread("../0-Data/1_intermediate_generated_data/annotated_ranking_dataset_binarized.csv")
attach(datacomplete)
print("table country")
table(datacomplete$country)

#--------------------------------------------
#Descriptive statistics on NDCG vs Ranking
#--------------------------------------------

datacomplete <- data.table::fread("../0-Data/1_intermediate_generated_data/ndcg_vs_ranking.csv")
attach(datacomplete)


#Descriptive statistics datacomplete
table(datacomplete$ndcg)
table(datacomplete$RankingFuncionPesos)


#Content ranking share per Country
table(datacomplete$ndcg,datacomplete$RankingFuncionPesos)

ggplot(datacomplete,
aes(x = RankingFuncionPesos, y = ndcg)) + 
geom_point() +
labs(x = "ranking", y = "ndcg") +
ggtitle("Ranking and ndcg") +
theme(plot.title = element_text(hjust = 0.5)) +
scale_y_continuous(breaks = seq(0, 1, 0.01)) 
#+ scale_x_continuous(label = scales::label_comma(accuracy = 1))

ggsave("plot.png")

sink()



