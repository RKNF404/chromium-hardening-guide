#!/usr/bin/python3

#  Copyright 2026 Rootkit404
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import sys
import os
import platform
import json
#import plistlib
import argparse
from enum import StrEnum

# Enums
class System(StrEnum):
    LIN = 'linux'
    WIN = 'windows'
    MAC = 'macos'
class SystemFilter(StrEnum):
    LIN = 'LINUX_ONLY'
    WIN = 'WINDOWS_ONLY'
    MAC = 'MACOS_ONLY'
class ConfigOption(StrEnum):
    ALL = 'all'
    CMDLINE = 'commandline'
    POLICY = 'policy'
class ConfigType(StrEnum):
    FEAT = 'Feature'
    FLAG = 'Flag'
    POL = 'Policy'
class FlagFileFormat(StrEnum):
    GENERIC = 'generic'
    VARIABLE = 'variable'

# Globals
Files = {
    'flags': 'flags/80-hardening-guide-flags.conf',
    'linux_policy': 'policy/80-hardening-guide-policy.json',
    'linux_recommended_policy': 'recommended-policy/81-hardening-guide-policy-recommended.json',
    'macos_policy': 'policy/com.google.Chrome.plist',
    'macos_recommended_policy': 'recommended-policy/com.google.Chrome.plist',
    'windows_policy': 'policy/hardening-guide-policy.reg',
    'windows_recommended_policy': 'recommended-policy/hardening-guide-recommended-policy.reg'
}

# Parse input file into a dictionary structure
def ParseConfigFile(dbFile):
    data = {}
    with open(dbFile, 'r') as config_data:
        try:
            data = json.load(config_data)
        except Exception as err:
            print('ERROR: parsing JSON db failed')
            print(err)
    return data

# Generate flags file
def WriteFlagsFile(fileFormat, flags):
    if not os.path.exists('flags'):
        os.makedirs('flags')
    with open(Files['flags'], 'w') as flagsOutput:
        if fileFormat == FlagFileFormat.VARIABLE:
            flagsOutput.write('CHROMIUM_FLAGS="' + '"\nCHROMIUM_FLAGS+=" '.join(flags) + '"')
        else:
            flagsOutput.write('\n'.join(flags))
    return

# Generate Linux policy file
# Recommend here will determine if the policies should be separated, if true they will be
def WriteJsonPolicy(recommend, policies, recommendedPolicies):
    if not recommend:
        policies.update(recommendedPolicies)
    else:
        if not os.path.exists('recommended-policy'):
            os.makedirs('recommended-policy')
        with open(Files['linux_recommended_policy'], 'w') as policyOutput:
            json.dump(recommendedPolicies, policyOutput, indent=4)
    if not os.path.exists('policy'):
        os.makedirs('policy')
    with open(Files['linux_policy'], 'w') as policyOutput:
        json.dump(policies, policyOutput, indent=4)
    return

def ConvertToReg(value):
    vt = type(value)
    match vt:
        case _:
            print(vt)

# Generate a reg policy file for Windows
def WriteRegPolicy(recommend, policies, recommendedPolicies):
    raise NotImplementedError('Windows registry policy generation not implemented')
    ### WILL NOT HIT
    if not recommend:
        policies.update(recommendedPolicies)
    with open(Files['windows_policy'], 'a') as policyOutput:
        json.dump(policies, policyOutput, indent=4)
    return

# Generate MacOS policy file
def WritePlistPolicy(recommend, policies, recommendedPolicies):
    raise NotImplementedError('MacOS policy generation not implemented')
    ### WILL NOT HIT
    '''
    Should be simple with the plist library handler
    '''
    return

# Check if a certain config has a certain tag
def TagMatch(confEntry, tag):
    return not tag or tag.upper() in (t.upper() for t in confEntry['Tags'])

def TypeMatch(confEntry, confOption):
    confType = confEntry['Type']
    match confOption.lower():
        case ConfigOption.ALL:
            return True
        case ConfigOption.CMDLINE:
            return confType == ConfigType.FEAT or confType == ConfigType.FLAG
        case ConfigOption.POLICY:
            return confType == ConfigType.POL
    return False

# General parsing and filtering
def ParseConfig(data, args):
    filteredData = {}
    optionalConfigs = []

    match args.system.lower():
        case System.LIN:
            systemFilter = [SystemFilter.WIN, SystemFilter.MAC]
        case System.WIN:
            systemFilter = [SystemFilter.LIN, SystemFilter.MAC]
        case System.MAC:
            systemFilter = [SystemFilter.WIN, SystemFilter.LIN]

    # Filter by tag and platform
    for e in data:
        if (
            TagMatch(data[e], args.tag) and
            not TagMatch(data[e], systemFilter[0]) and
            not TagMatch(data[e], systemFilter[1])
        ):
            filteredData[e] = data[e]

    # Find all potentially negated configs, figure out if they are actually negated later
    tempFiltData = dict(filteredData)
    for e in filteredData:
        configEntry = filteredData[e]['Configs']
        for c in configEntry:
            if 'OPTIONAL' not in filteredData[e]['Tags'] and 'Negates' in configEntry[c] and TypeMatch(configEntry[c], args.type):
                for n in configEntry[c]['Negates']:
                    if n in tempFiltData:
                        del tempFiltData[n]

        # Store that the config is optional, only if it hasn't been removed yet
        if 'OPTIONAL' in filteredData[e]['Tags'] and e in tempFiltData:
            optionalConfigs.append(e)

    # Update the filtered dictionary
    filteredData = tempFiltData

    for e in optionalConfigs:
        if e in filteredData:
            for i in range(5):
                if args.choice == '':
                    print(filteredData[e]['Option'] + ' [Y/n]')
                    yn = input()
                    match yn.lower():
                        case 'y' | 'yes' | '':
                            # remove negations
                            tempFiltData = dict(filteredData)
                            configEntry = filteredData[e]['Configs']
                            for c in configEntry:
                                if 'Negates' in configEntry[c]:
                                    for n in configEntry[c]['Negates']:
                                        if n in tempFiltData:
                                            del tempFiltData[n]
                            filteredData = tempFiltData
                            break
                        case 'n' | 'no':
                            del filteredData[e]
                            break
                        case _:
                            print('WARNING: improper input, either hit enter for "Y" or choices are : ["y", "n", "yes", "no"]')
                else:
                    yn = args.choice
                    break
            else:
                del filteredData[e]

    if args.choice == '' or args.choice == 'y':
        # Find remaining negations
        tempFiltData = dict(filteredData)
        for e in filteredData:
            configEntry = filteredData[e]['Configs']
            for c in configEntry:
                if 'OPTIONAL' in filteredData[e]['Tags'] and 'Negates' in configEntry[c] and TypeMatch(configEntry[c], args.type):
                    for n in configEntry[c]['Negates']:
                        if n in tempFiltData:
                            del tempFiltData[n]

        # We have a completed configuration file with all negations removed, and all choices made
        filteredData = tempFiltData

    # Generate the configuration data structures
    flags = []
    enableFeatures = []
    disableFeatures = []
    policies = {}
    recommendedPolicies = {}
    for e in filteredData:
        entry = filteredData[e]
        for c in entry['Configs']:
            config = entry['Configs'][c]
            match config['Type']:
                case ConfigType.POL:
                    if 'Recommendable' in config and config['Recommendable']:
                        recommendedPolicies[c] = config['Value']
                    else:
                        policies[c] = config['Value']
                case ConfigType.FEAT:
                    if config['Enable']:
                        enableFeatures.append(c)
                    else:
                        disableFeatures.append(c)
                case ConfigType.FLAG:
                    flag = '--' + c
                    if 'Arguments' in config:
                        flag += '=' + ','.join(config['Arguments'])
                    flags.append(flag)

    # Append features as flags
    if enableFeatures:
        flags.append('--enable-features=' + ','.join(enableFeatures))
    if disableFeatures:
        flags.append('--disable-features=' + ','.join(disableFeatures))

    # Cleanup files
    for f in Files:
        if os.path.isfile(Files[f]):
            os.remove(Files[f])

    # Write to disk
    if args.type in [ConfigOption.CMDLINE, ConfigOption.ALL]:
        WriteFlagsFile(args.format, flags)

    if args.type in [ConfigOption.POLICY, ConfigOption.ALL]:
        recommendable = args.recommended == 'y'
        match args.system.lower():
            case System.LIN:
                WriteJsonPolicy(recommendable, policies, recommendedPolicies)
            case System.WIN:
                WriteRegPolicy(recommendable, policies, recommendedPolicies)
            case System.MAC:
                WritePlistPolicy(recommendable, policies, recommendedPolicies)
    return

def main() -> int:
    platform_os = platform.system()
    if platform_os == 'Darwin':
        platform_os = System.MAC

    parser = argparse.ArgumentParser(
        prog='ConfigGen',
        description='Parse a chromium policy and flag database (Configuration.json), outputs flags to a folder `flags/`, outputs policies to a folder `policy/`, and recommended policies to a folder `recommended-policy/` in the current working directory.'
    )
    parser.add_argument(
        '--system', '-s',
        choices=[System.LIN, System.WIN, System.MAC],
        default=platform_os,
        help='Target operating system (if not specified, then current platform), MacOS and Windows not supported currently.'
    )
    parser.add_argument(
        '--type', '-t',
        choices=[ConfigOption.ALL, ConfigOption.CMDLINE, ConfigOption.POLICY],
        default=ConfigOption.ALL,
        help='Type of configuration for output file (if not specified then all).'
    )
    parser.add_argument(
        '--format',
        choices=[FlagFileFormat.GENERIC, FlagFileFormat.VARIABLE],
        default=FlagFileFormat.GENERIC,
        help='Output format for the flag file. Generic is just each flag separated by a new line, Variable is in the form of shell variable declarations, Chromewrapper is in the form of my chromewrapper project\'s wrapper flags file. If not specified then generic.')
    parser.add_argument(
        '--tag',
        help='Filter by tag for the output config.'
    )
    parser.add_argument(
        '--file', '-f',
        default='Configuration.config',
        help='Path to configuration file. Defaults to `Configuration.config`'
    )
    parser.add_argument(
        '--choice', '-c',
        choices=['y', 'n', ''],
        default='',
        help='Set the default choice for optional input. If unspecified, then each optional will be asked.'
    )
    parser.add_argument(
        '--recommended', '-r',
        default='n',
        choices=['y', 'n'],
        help='Separate recommended policies from regular ones.'
    )
    args = parser.parse_args()
    
    if args.system.lower() == System.WIN:
        args.format = FlagFileFormat.GENERIC

    if args.system.lower() == System.MAC:
        print('TODO: ' + args.system + ' support not implemented')
        return 1

    if not os.path.isfile(args.file):
        print('ERROR: file "' + args.file + '" does not exist')
        return 1

    data = ParseConfigFile(args.file)
    if not data:
        print('ERROR: parsed data is empty')
        return 1

    ParseConfig(data, args)

    return 0

if __name__ == "__main__":
    sys.exit(main())
