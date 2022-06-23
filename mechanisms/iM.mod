TITLE Mod file for component: Component(id=iM type=ionChannelHH)

COMMENT

    This NEURON file has been generated by org.neuroml.export (see https://github.com/NeuroML/org.neuroml.export)
         org.neuroml.export  v1.5.4
         org.neuroml.model   v1.5.4
         jLEMS               v0.9.9.1

ENDCOMMENT

NEURON {
    SUFFIX iM
    USEION k WRITE ik VALENCE 1 ? Assuming valence = 1; TODO check this!!
    
    RANGE gion                           
    RANGE gmax                              : Will be changed when ion channel mechanism placed on cell!
    RANGE conductance                       : parameter

    
    RANGE fopen                             : exposure
    RANGE m_instances                       : parameter
    
    RANGE m_tau                             : exposure
    :GLOBAL m_min    
    RANGE m_inf                             : exposure
    
    RANGE m_rateScale                       : exposure
    
    RANGE m_fcond                           : exposure
    RANGE m_timeCourse_TIME_SCALE           : parameter
    RANGE m_timeCourse_VOLT_SCALE           : parameter
    
    RANGE m_timeCourse_t                    : exposure
    RANGE m_steadyState_rate                : parameter
    RANGE m_steadyState_midpoint            : parameter
    RANGE m_steadyState_scale               : parameter
    
    RANGE m_steadyState_x                   : exposure
    RANGE m_q10Settings_q10Factor           : parameter
    RANGE m_q10Settings_experimentalTemp    : parameter
    RANGE m_q10Settings_TENDEGREES          : parameter
    
    RANGE m_q10Settings_q10                 : exposure
    RANGE m_timeCourse_V                    : derived variable
    RANGE m_tauUnscaled                     : derived variable
    RANGE conductanceScale                  : derived variable
    RANGE fopen0                            : derived variable
    RANGE gmin
    RANGE shift

    RANGE m_min
    
    RANGE i_output                            
    RANGE output
    GLOBAL m_timeCourse_TIME_SCALE
}

UNITS {
    
    (nA) = (nanoamp)
    (uA) = (microamp)
    (mA) = (milliamp)
    (A) = (amp)
    (mV) = (millivolt)
    (mS) = (millisiemens)
    (uS) = (microsiemens)
    (molar) = (1/liter)
    (kHz) = (kilohertz)
    (mM) = (millimolar)
    (um) = (micrometer)
    (umol) = (micromole)
    (S) = (siemens)
    
}

PARAMETER {
    
    gmax = 0  (S/cm2)                       : Will be changed when ion channel mechanism placed on cell!
    gmin = 0  (S/cm2)
    
    conductance = 1.0E-5 (uS)
    m_instances = 1 
    m_timeCourse_TIME_SCALE = 1 (ms)
    m_timeCourse_VOLT_SCALE = 1 (mV)
    m_steadyState_rate = 1 
    m_steadyState_midpoint = -36.7 (mV)
    m_steadyState_scale = 9.48 (mV)
    m_q10Settings_q10Factor = 2.6
    m_q10Settings_experimentalTemp = 308.15 (K)
    m_q10Settings_TENDEGREES = 10 (K)
    shift=3 (mV)
    :m_min=0
}

ASSIGNED {
    
    gion   (S/cm2)                          : Transient conductance density of the channel? Standard Assigned variables with ionChannel
    v (mV)
    celsius (degC)
    temperature (K)
    ek (mV)
    ik (mA/cm2)

    g
    
    
    m_timeCourse_V                         : derived variable
    
    m_timeCourse_t (ms)                    : derived variable
    
    m_steadyState_x                        : derived variable
    
    m_q10Settings_q10                      : derived variable
    
    m_rateScale                            : derived variable
    
    m_fcond                                : derived variable
    
    m_inf                                  : derived variable
    
    m_tauUnscaled (ms)                     : derived variable
    
    m_tau (ms)                             : derived variable
    
    conductanceScale                       : derived variable
    
    fopen0                                 : derived variable
    
    fopen                                  : derived variable
    
    rate_m_q (/ms)

    m_min



    output
    i_output  
}

STATE {
    m_q  
    
}

INITIAL {
    ek = -90.0
    
    temperature = celsius + 273.15
    
    rates()
    rates() ? To ensure correct initialisation.
    
    m_q = m_inf
    m_min = gmin/gmax




    output   = gmax * (m_min+m_q)
    i_output = output * (v - ek)

    ik = i_output


    
}

BREAKPOINT {
    
    SOLVE states METHOD cnexp
    
    ? DerivedVariable is based on path: conductanceScaling[*]/factor, on: Component(id=iM type=ionChannelHH), from conductanceScaling; null
    ? Path not present in component, using factor: 1
    
    conductanceScale = 1 
    
    ? DerivedVariable is based on path: gates[*]/fcond, on: Component(id=iM type=ionChannelHH), from gates; Component(id=m type=gateHHtauInf)
    ? multiply applied to all instances of fcond in: <gates> ([Component(id=m type=gateHHtauInf)]))
    fopen0 = m_fcond ? path based, prefix = 
    
    fopen = conductanceScale  *  fopen0 ? evaluable
    g = conductance  *  fopen   ? evaluable



    gion = g


    

    output   = gmax * (m_min+m_q)
    i_output = output * (v - ek)

    ik = i_output

    
    



    
    
}

DERIVATIVE states {
    rates()
    m_q' = rate_m_q 
    
}

PROCEDURE rates() {
    
    m_timeCourse_V = v /  m_timeCourse_VOLT_SCALE ? evaluable
    m_timeCourse_t = (13.4+26.3*exp(    -( ( m_timeCourse_V -29.7+shift)/30.3 ) * ( ( m_timeCourse_V -29.7+shift)/30.3 )   )) *  m_timeCourse_TIME_SCALE ? evaluable
    m_steadyState_x = m_steadyState_rate  / (1 + exp(0 - (v -  m_steadyState_midpoint +shift)/ m_steadyState_scale )) ? evaluable
    m_q10Settings_q10 = m_q10Settings_q10Factor ^((temperature -  m_q10Settings_experimentalTemp )/ m_q10Settings_TENDEGREES ) ? evaluable
    ? DerivedVariable is based on path: q10Settings[*]/q10, on: Component(id=m type=gateHHtauInf), from q10Settings; Component(id=null type=q10ExpTemp)
    ? multiply applied to all instances of q10 in: <q10Settings> ([Component(id=null type=q10ExpTemp)]))
    m_rateScale = m_q10Settings_q10 ? path based, prefix = m_
    
    m_fcond = m_q ^ m_instances ? evaluable
    ? DerivedVariable is based on path: steadyState/x, on: Component(id=m type=gateHHtauInf), from steadyState; Component(id=null type=HHSigmoidVariable)
    m_inf = m_steadyState_x ? path based, prefix = m_
    
    ? DerivedVariable is based on path: timeCourse/t, on: Component(id=m type=gateHHtauInf), from timeCourse; Component(id=null type=iM_m_tau)
    m_tauUnscaled = m_timeCourse_t ? path based, prefix = m_
    
    m_tau = m_tauUnscaled  /  m_rateScale ? evaluable
    
     
    rate_m_q = ( m_inf  -  m_q ) /  m_tau ? Note units of all quantities used here need to be consistent!
    
     
    
     
    
     
    
     
    
}

