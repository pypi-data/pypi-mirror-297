#ifndef IG_ALIGNERS_HEADER_H
#define IG_ALIGNERS_HEADER_H

#include <nanobind/nanobind.h>
#include <nanobind/ndarray.h>
#include <vector>
#include <string>
#include <algorithm>
#include <filesystem>
#include <tuple>
#include <set>
#include <array>
#include <memory>
#include "../utilities/consensus_file_utilities.h"
#include "../utilities/utilities.h"
#include "../numbering_constants.h"



// Codes for the pathways that can link a score
// to the best-scoring parent.
#define LEFT_TRANSFER 1
#define UP_TRANSFER 2
#define DIAGONAL_TRANSFER 0

// The columns of the score matrix that are accessed for gap penalties.
#define QUERY_GAP_COLUMN 21
#define TEMPLATE_GAP_COLUMN 22


namespace nb = nanobind;


class IGAligner {
    public:
        IGAligner(std::string consensus_filepath,
                std::string chainName, std::string scheme,
                double terminalTemplateGapPenalty,
                double CterminalQueryGapPenalty,
                bool compress_initial_gaps);
        void align(std::string query_sequence, int *encoded_sequence,
                std::vector<std::string> &final_numbering,
                double &percent_identity, std::string &error_message);
        std::string get_chain_name();

        void _test_fill_needle_scoring_table(std::string query_sequence,
                    nb::ndarray<double, nb::shape<-1,-1>, nb::device::cpu, nb::c_contig> scoreMatrix,
                    nb::ndarray<uint8_t, nb::shape<-1,-1>, nb::device::cpu, nb::c_contig> pathTraceMat);

        // Allowed error codes. These will be mapped to strings which explain in more detail.
        enum allowedErrorCodes {noError = 0, invalidSequence = 1, fatalRuntimeError = 2,
            tooManyInsertions  = 3, alignmentWrongLength = 4,
            unacceptableConservedPositions = 5};


    protected:
        // Default gap penalties for gaps at the beginning and end of the sequence.
        // template is a weak penalty for placing gaps outside the numbering,
        // while query is a weak penalty for placing gaps in the numbering
        // (i.e. skipping numbers).

        const std::string chain_name;
        std::string scheme;
        double terminalTemplateGapPenalty;
        double CterminalQueryGapPenalty;
        bool compress_initial_gaps;

        std::unique_ptr<double[]> score_array;
        size_t score_arr_shape[2];
        int num_positions;
        int num_restricted_positions;

        std::vector<std::set<char>> consensus_map;
        std::vector<int> highly_conserved_positions;
        std::array<std::string, 6> error_code_to_message {{"",
                "Sequence contains invalid characters",
                "Fatal runtime error in IGAligner. Unusual. Please report",
                "> max allowed insertions -- suggests alignment error or unusual sequence",
                "Alignment length != length of input sequence. Unusual. Please report.",
                "Unexpected AA at conserved position."}};


        // Alphabet for numbering insertions. Our preference would be to number insertions
        // as _1, _2 etc, but most numbering programs use letters, so we do the same here
        // for consistency and ease of comparison. This does limit the number of possible
        // insertions BUT if there is ever a case where more than 70 insertions have occurred
        // at some point in the sequence, there is almost certainly an error in the alignment, and
        // that's how we handle this eventuality if it occurs. (Indeed, it is very rare to have
        // more than a few at any given position, so the size of alphabet here is overkill.)
        const std::vector<std::string> alphabet = {"A", "B", "C", "D", "E", "F", "G", "H", "I",
                                    "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U",
                                    "V", "W", "X", "Y", "Z", "AA", "BB", "CC", "DD", "EE",
                                    "FF", "GG", "HH", "II", "JJ", "KK", "LL", "MM", "NN",
                                    "OO", "PP", "QQ", "RR", "SS", "TT", "UU", "VV",
                                    "WW", "XX", "YY", "ZZ", "AAA", "BBB", "CCC", "DDD", 
                                    "EEE", "FFF", "GGG", "HHH", "III", "JJJ", "KKK", "LLL",
                                    "MMM", "NNN", "OOO", "PPP", "QQQ", "RRR", "SSS", "TTT",
                                    "UUU", "VVV", "WWW", "XXX", "YYY", "ZZZ"};
        
        void fill_needle_scoring_table(uint8_t *path_trace,
                    int query_seq_len, int row_size,
                    const int *encoded_sequence,
                    int &numElements);

};

#endif
