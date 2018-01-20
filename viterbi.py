import sys

prob = {}
sente =[] 

def process_sente(name):
    # note that debug info should be printed to stderr
    # sys.stderr.write('[process_file]\tprocessing file: %s\n' % (path))
	fp = open(name, "r")
	for line in fp:
		sente.append(line)
		words = line.split()
	return 0

def process_prob(name):
    # note that debug info should be printed to stderr
    # sys.stderr.write('[process_file]\tprocessing file: %s\n' % (path))
	fp = open(name, "r")
	for line in fp:

		words = line.split()
		key = words[0]+" "+words[1]
		prob[key] = float(words[2])

	return 0


	
def viterbi():
	viterbi_path = []
	pi0 = 1 #initial : set pi(0,*)=1
	pi = []
	pi_forward = []
	POS_tags = ['noun', 'verb', 'inf', 'prep']
	for line in sente:
		print '\nPROCESSING SENTENCE:%s' % line
		words = line.split()
		for i in range(len(words)):
			pi_prob = []
			pi_forward_prob = []
			bkptr = []
			for j in range(4): #index def:0->noun, 1->verb, 2->inf, 3->prep
				
				if i == 0:
					transition = POS_tags[j]+" "+"phi"
					emission = words[i]+" "+POS_tags[j]
					if transition not in prob:
						prob[transition] = 0.0001
					if emission not in prob:
						prob[emission] = 0.0001
					pi_prob.append(pi0 * prob[transition] * prob[emission])
					pi_forward_prob.append(pi0 * prob[transition] * prob[emission])
				else:
					pi_prob_prev = []
					
					for k in range(4):
						
						transition = POS_tags[j]+" "+POS_tags[k]
						emission = words[i]+" "+POS_tags[j]
						if transition not in prob:
							prob[transition] = 0.0001
							#print transition
						if emission not in prob:
							#print emission
							prob[emission] = 0.0001
						
						#print pi[i-1][k]
						pi_prev = pi[i-1][k] #FixMe
						pi_prob_prev.append(pi_prev * prob[transition] * prob[emission])
					pi_prob.append(max(pi_prob_prev))
					pi_forward_prob.append(sum(pi_prob_prev))
					bkptr.append(POS_tags[pi_prob_prev.index(max(pi_prob_prev))])#store the backpointer
					#print bkptr
					#pi_prob_prev[:] = []
			pi.append(pi_prob)
			pi_forward.append(pi_forward_prob)
			
			viterbi_path.append(bkptr)
			
		#print pi 
		print "\nFINAL VITERBI NETWORK"
		for i in range(len(words)):
			for j in range(4):
				print 'P(%s|%s) = %.10f ' % (words[i],POS_tags[j],pi[i][j])
		print "\nFINAL BACKPTR NETWORK"

		for i in range(1,len(words)):
			#viterbi_ntwk = []
			#viterbi_ntwk.append(viterbi_path[i+1])
			#print viterbi_path
			#print viterbi_ntwk
			#viterbi_ntwk = viterbi_path[i]
			for j in range(4):
				print 'Backptr(%s=%s) = %s' % (words[i],POS_tags[j],viterbi_path[i][j])				
		
		#stop sign (fin) probability index		
		stop_sign_prob = "fin"+" "+POS_tags[pi[len(words)-1].index(max(pi[len(words)-1]))]
		if stop_sign_prob not in prob:
			prob[stop_sign_prob] = 0.0001
					
		print "\nBEST TAG SEQUENCE HAS PROBABILITY= %.10f" % float(max(pi[len(words)-1]) * prob[stop_sign_prob])
		#print pi
		#print viterbi_path
		for i in range(len(words)):
			if i == 0:
				print "%s->%s" % (words[len(words)-i-1],POS_tags[pi[len(words)-i-1].index(max(pi[len(words)-i-1]))])
				idx = pi[len(words)-i-1].index(max(pi[len(words)-i-1]))
			else:
				print "%s->%s" % (words[len(words)-i-1],viterbi_path[len(words)-i][idx])#POS_tags[pi[len(words)-i-1].index(max(pi[len(words)-i-1]))])
				idx = POS_tags.index(viterbi_path[len(words)-i][idx])
		#print pi_forward
		print "\nFORWARD ALGORITHM RESULTS"
		for i in range(len(words)):
			for j in range(4):
				print 'P(%s|%s) = %.10f ' % (words[i],POS_tags[j],pi_forward[i][j])

		pi[:] = []
		pi_forward[:] = []	
		viterbi_path[:] = []
	
	
def main(prob_file, sente_file):
	process_sente(sente_file)
	process_prob(prob_file)

	#print prob
	#print sente
	
	viterbi()
	


if __name__ == '__main__':
    if (len(sys.argv) != 3):
        print 'usage:\tviterbi.py <probabilities file> <sentences file>'
        sys.exit(0)
    main(sys.argv[1],sys.argv[2])