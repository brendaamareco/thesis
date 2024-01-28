library(ggplot2)
library(data.table)

df <- fread("../0-Data/1_intermediate_generated_data/annotated_ranking_dataset.csv")

ggplot(df, aes(x = country, fill = category)) +
  geom_bar(position = "dodge") +
  labs(title = "Category Distribution by Country",
       x = "Country",
       y = "Category") +
  scale_fill_manual(values = c("isBugReport" = "red", "isFeatureShortcoming/isFeatureRequest" = "blue", "Other" = "green")) +
  theme_minimal() +
  theme(legend.position = "bottom")

ggsave("category_country_plot.png")

print(p) 


