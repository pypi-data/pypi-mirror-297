#ifndef PAIRED_CHAIN_ANNOTATOR_HEADER_H
#define PAIRED_CHAIN_ANNOTATOR_HEADER_H

#include <vector>
#include <string>
#include <algorithm>
#include <tuple>
#include <set>
#include <array>
#include "cterm_finder.h"
#include "annotator_base_class.h"
#include "single_chain_annotator.h"
#include "../numbering_constants.h"






class PairedChainAnnotatorCpp : public AnnotatorBaseClassCpp {
    public:
        PairedChainAnnotatorCpp(std::string scheme = "imgt",
                std::string consensus_filepath = "");

        std::pair<std::tuple<std::vector<std::string>, double, std::string, std::string>,
            std::tuple<std::vector<std::string>, double, std::string, std::string>>
            analyze_seq(std::string sequence);
        std::tuple<std::vector<std::tuple<std::vector<std::string>, double, std::string, std::string>>,
            std::vector<std::tuple<std::vector<std::string>, double, std::string, std::string>>>
            analyze_seqs(std::vector<std::string> sequences);


    protected:
        std::string scheme;

        std::unique_ptr<SingleChainAnnotatorCpp> light_chain_analyzer;
        std::unique_ptr<SingleChainAnnotatorCpp> heavy_chain_analyzer;
        std::unique_ptr<SingleChainAnnotatorCpp> analyzer;
};

#endif
