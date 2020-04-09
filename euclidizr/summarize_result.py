

def summary_result(fit_mod):

	dict={}

	dict['flux']=fit_mod.flux[0]
	dict['r_eff']=fit_mod.r_eff[0]
	dict['n']=fit_mod.n[0]
	dict['x_0']=fit_mod.x_0[0]
	dict['y_0']=fit_mod.y_0[0]
	dict['g1']=fit_mod.g1[0]
	dict['g2']=fit_mod.g2[0]

	return dict
