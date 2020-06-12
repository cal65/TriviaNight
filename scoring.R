library(googlesheets4)
library(googledrive)
library(data.table)
library(ggplot2)
library(ggthemes)
library(fuzzywuzzyR)
library(stringr)
options(stringsAsFactors = F)
setwd('~/Documents/CAL/Real_Life/Blog Posts/TriviaNight/')
sheet_results <- drive_find(type = "spreadsheet")
#sheet lookups by name
id1 <- sheet_results[which(sheet_results$name == "Trivia June 2020 (Responses)"),]$id
id2 <- sheet_results[which(sheet_results$name == "Trivia - Round 2 (Responses)"),]$id
id_answers <- sheet_results[which(sheet_results$name == "Trivia June 2020 - Answers"),]$id
resp1 <- setDT(read_sheet(id1))
resp2<- setDT(read_sheet(id2))
answers <- setDT(read_sheet(id_answers))


## Round 1
# renaming 
names(resp1) <- mapvalues(names(resp1), from = "What is your team name?", to = "Name")
#reshaping data and dropping timestamp column so that we can add a new Graded column
resp1.m <- melt(resp1[,-1], id = 'Name', variable.name = 'Question', value.name = 'Answer')
#extract number from the question string
resp1.m$Number <- as.numeric(unlist(
  lapply(
    str_split(string = resp1.m$Question, pattern = '\\.'), function(x) x[1]))
)
#initiate T/F column
resp1.m$Correct <- logical(length = nrow(resp1.m))
resp1.m$Question <- factor(resp1.m$Question, 
                           levels = unique(resp1.m$Question))
answers1 <- answers[Round == 1]

for (i in 1:10){
  for (team_name in unique(resp1.m$Name)){
    corrects <- GetCloseMatches(answers1$Answer[i], resp1.m[Number == i]$Answer)
    #additionally, if the answer is not a close match but is contained within the true answer, it should count
    additional <- unique(grep(answers1$Answer[i], resp1.m[Number == i]$Answer, 
                              value=T, ignore.case = T))
    for (answer in resp1.m[Number == i]$Answer){
      #grepl should work, unless answer is NA. The %in% deals with NA answers
      if (grepl(answer, answers1$Answer[i]) %in% T) { 
        additional <- append(additional, answer)
      }
    }
    corrects <- unique(c(corrects, additional))
    resp1.m[Number == i]$Correct <- resp1.m[Number == i]$Answer %in% corrects
  }
}

#break questions into multiple lines for readability in graph
str_len <- 40
resp1.m$Question_Formatted <- character(length = nrow(resp1.m))
for (i in 1:nrow(resp1.m)){
  resp1.m$Question_Formatted[i] <- paste(stri_wrap(resp1.m$Question[i], width=str_len), collapse='\n')
}
resp1.m$Question_Formatted <- factor(resp1.m$Question_Formatted,
                                     levels = rev(unique(resp1.m$Question_Formatted)))
#plot
ggplot(resp1.m) + geom_tile(aes(x=Name, y=Question_Formatted, fill=Correct), color='black') +
  geom_text(aes(x=Name, y=Question_Formatted, label = Answer)) +
  scale_fill_brewer(palette = 'Set2') +
  ylab('Question') +
  ggtitle('Responses - Round 1')
ggsave('Responses_Round1.jpeg', width= 12, height=9)

names(resp2) <- mapvalues(names(resp2), from = "What is your team name?", to = "Name")
resp2.m <- melt(resp2[,-1], id = 'Name', variable.name = 'Question', value.name = 'Answer')
resp2.m$Number <- as.numeric(unlist(
  lapply(
    str_split(string = resp2.m$Question, pattern = '\\.'), function(x) x[1])
)
)
resp2.m$Correct <- logical()
answers2 <- answers[Round == 2]
for (i in 1:10){
  corrects <- GetCloseMatches(answers2[Number == i]$Answer, resp2.m[Number == i]$Answer)
  resp2.m[Number == i]$Correct <- resp2.m[Number == i]$Answer %in% corrects
}






